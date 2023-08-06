from rdflib.graph import Graph
from rdflib.store import Store, VALID_STORE, NO_STORE
from rdflib.term import URIRef, BNode, Literal, Variable
from urlparse import urlparse
from traceback import format_exc
import pyodbc

__all__ = ['Virtuoso']

log = __import__("logging").getLogger(__name__)

class Virtuoso(Store):
    context_aware = True
    transaction_aware = True
    def open(self, dsn):
        try:
            self._connection = pyodbc.connect(dsn)
            self._cursor = self._connection.cursor()
            log.info("Virtuoso Store Connected: %s" % dsn)
            return VALID_STORE
        except:
            log.error("Virtuoso Connection Failed:\n%s" % format_exc())
            return NO_STORE

    def close(self, commit_pending_transaction=False):
        if commit_pending_transaction:
            self.commit()
        else:
            self.rollback()
        self._connection.close()

    def query(self, q):
        return self._cursor.execute(str(q))

    def sparql_query(self, q):
        return self.query(u"SPARQL " + q)
    
    def commit(self):
        self.query("COMMIT WORK")
    def rollback(self):
        self.query("ROLLBACK WORK")

    def contexts(self, statement=None):
        if statement is None:
            q = (u'SELECT DISTINCT __ro2sq(G) FROM RDF_QUAD')
        else:
            q = (u'SELECT DISTINCT ?g WHERE '            
                 u'{ GRAPH ?g { %(S)s %(P)s %(O)s } }')
            q = _query_bindings(statement)
        for uri, in self.query(q):
            yield Graph(self, identifier=URIRef(uri))
            
    def triples(self, statement, context=None):
        query_bindings = _query_bindings(statement, context)
        for k,v in query_bindings.items():
            if v.startswith('?') or v.startswith('$'):
                query_bindings[k+"v"]=v
            else:
                query_bindings[k+"v"]="(%s) AS %s" % (v, Variable(k).n3())
        q = (u'SPARQL define output:valmode "LONG" '
             u'SELECT DISTINCT %(Sv)s %(Pv)s %(Ov)s %(Gv)s '
             u'WHERE { GRAPH %(G)s { %(S)s %(P)s %(O)s } }')
        q = q % query_bindings
        log.debug(q)

        resolver = self._connection.cursor()
        for result in self.query(q):
            s,p,o,g = [resolve(resolver, x) for x in result]
            yield (s,p,o), g
        resolver.close()

    def add(self, statement, context=None, quoted=False):
        assert not quoted, "No quoted graph support in Virtuoso store yet, sorry"
        query_bindings = _query_bindings(statement, context)
        q = u'SPARQL INSERT '
        if context is not None:
            q += u'INTO GRAPH %(G)s ' % query_bindings
        q += u'{ %(S)s %(P)s %(O)s }' % query_bindings
        log.debug(q)
        self.query(q)

    def remove(self, statement, context=None, quoted=False):
        assert not quoted, "No quoted graph support in Virtuoso store yet, sorry"
        query_bindings = _query_bindings(statement, context)
        q = u'SPARQL DELETE '
        if context is not None:
            q += u'FROM GRAPH %(G)s ' % query_bindings
        q += u'{ %(S)s %(P)s %(O)s }' % query_bindings
        log.debug(q)
        self.query(q)

def _bnode_to_nodeid(bnode):
    from string import ascii_letters
    iri = bnode
    for c in bnode[1:]:
        if c in ascii_letters:
            # from rdflib
            iri = "b" + "".join(str(ord(x)-38) for x in bnode)
    return URIRef("nodeID://%s" % iri)

def _nodeid_to_bnode(iri):
    from string import digits
    iri = iri[9:] # strip off "nodeID://"
    bnode = iri
    if len(iri) == 19:
        # assume we made it...
        ones, tens = iri[1::2], iri[2::2]
        chars = [x+y for x,y in zip(ones, tens)]
        bnode = "".join(str(chr(int(x)+38)) for x in chars)
    return BNode(bnode)

def resolve(resolver, (value, dvtype, flag, lang, dtype)):
    if dvtype in (129, 211):
        print "XXX", dtype, value, dtype
    if dvtype == pyodbc.VIRTUOSO_DV_IRI_ID:
        q = (u'SELECT __ro2sq(%s)' % value)
        resolver.execute(str(q))
        iri, = resolver.fetchone()
        if iri.startswith("nodeID://"):
            return _nodeid_to_bnode(iri)
        return URIRef(iri)
    if dvtype == pyodbc.VIRTUOSO_DV_RDF:
        return Literal(value, lang=lang or None, datatype=dtype or None)
    if dvtype == pyodbc.VIRTUOSO_DV_STRING:
        return Literal(value)
    if dvtype == pyodbc.VIRTUOSO_DV_LONG_INT:
        return Literal(int(value))
    if dvtype == pyodbc.VIRTUOSO_DV_DATETIME:
        return Literal(value.replace(" ", "T"),
                       datatype=URIRef("http://www.w3.org/2001/XMLSchema#dateTime"))
    if dvtype == pyodbc.VIRTUOSO_DV_DATE:
        return Literal(value, datatype=URIRef("http://www.w3.org/2001/XMLSchema#date"))
    log.warn("Unhandled SPASQL DV type: %d for %s" % (dvtype, value))
    return Literal(value)

def _query_bindings((s,p,o), g=None):
    if isinstance(g, Graph):
        g = g.identifier
    if s is None: s = Variable("S")
    if p is None: p = Variable("P")
    if o is None: o = Variable("O")
    if g is None: g = Variable("G")
    if isinstance(s, BNode):
        s = _bnode_to_nodeid(s)
    if isinstance(p, BNode):
        p = _bnode_to_nodeid(p)
    if isinstance(o, BNode):
        o = _bnode_to_nodeid(o)
    if isinstance(g, BNode):
        g = _bnode_to_nodeid(g)
    return dict(
        zip("SPOG", [x.n3() for x in (s,p,o,g)])
        )
