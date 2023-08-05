<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:atom="http://www.w3.org/2005/Atom"
    xmlns:rel="http://www.iana.org/assignments/relation/"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:dc="http://purl.org/dc/terms/"
    xmlns:dcam="http://purl.org/dc/dcam/"
    xmlns:str="http://exslt.org/strings"
    xmlns:foaf="http://xmlns.com/foaf/0.1/"
    xmlns:meta="http://oreilly.com/xslt/functions/meta"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:rdfatom="http://www.w3.org/2005/Atom#">
    <xsl:output indent="yes"/>

    <xsl:template match="/">
        <rdf:RDF>
            <xsl:apply-templates/>
        </rdf:RDF>
    </xsl:template>

    <xsl:template match="atom:feed" >
        <rdf:Description xml:lang="en" xml:base="{atom:link[@rel='self']/@href}">
            <xsl:attribute name="rdf:about">
                <xsl:value-of select="atom:link[@rel='self']/@href"/>
            </xsl:attribute>
            <xsl:element name="type" namespace="rdf">
                <xsl:attribute name="rdf:resource">
                    <xsl:value-of select="concat('http://www.w3.org/2005/Atom', 'feed')"/>
                </xsl:attribute>
            </xsl:element>
            <xsl:apply-templates/>
        </rdf:Description>
    </xsl:template>
    
    <xsl:template name="atom_entry_with_content">
        <xsl:variable name="metadata_location">
            <xsl:choose>
                <xsl:when test="atom:link[@rel='edit']"
                    ><xsl:value-of select="atom:link[@rel='edit']/@href" /></xsl:when>
                <xsl:otherwise
                    ><xsl:value-of select="atom:id"/></xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <rdf:Description xml:lang="en" xml:base="{$metadata_location}">
            <xsl:attribute name="rdf:about">
                <xsl:value-of select="atom:content/@src"/>
            </xsl:attribute>
            <xsl:element name="rdfs:isDefinedBy">
                <xsl:element name="rdf:Description">
                    <xsl:attribute name="rdf:about"><xsl:value-of select="$metadata_location"/></xsl:attribute>
                    <xsl:element name="rdf:type">
                        <xsl:attribute name="rdf:resource">
                            <xsl:value-of select="concat('http://www.w3.org/2005/Atom#', 'entry')"/>
                        </xsl:attribute>
                    </xsl:element>
                </xsl:element>
            </xsl:element>
            <xsl:apply-templates/>
        </rdf:Description>
    </xsl:template>
    
    <xsl:template name="atom_entry">
        <xsl:variable name="metadata_location">
            <xsl:choose>
                <xsl:when test="atom:link[@rel='edit']"
                    ><xsl:value-of select="atom:link[@rel='edit']/@href" /></xsl:when>
                <xsl:otherwise
                    ><xsl:value-of select="atom:id"/></xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <rdf:Description xml:lang="en" xml:base="{$metadata_location}">
            <xsl:attribute name="rdf:about">
                <xsl:value-of select="$metadata_location"/>
            </xsl:attribute>
            <xsl:element name="rdf:type">
                <xsl:attribute name="rdf:resource">
                    <xsl:value-of select="concat('http://www.w3.org/2005/Atom#', 'entry')"/>
                </xsl:attribute>
            </xsl:element>
            <xsl:apply-templates/>
        </rdf:Description>
    </xsl:template>

    <xsl:template match="atom:entry[atom:content/@src]">
        <xsl:call-template name="atom_entry_with_content"/>
    </xsl:template>

    <xsl:template match="atom:entry[not(atom:content/@src)]">
        <xsl:call-template name="atom_entry"/>
    </xsl:template>

    <xsl:template match="atom:entry[atom:content/@src][parent::atom:feed]">
        <dc:hasPart>
            <xsl:call-template name="atom_entry_with_content"/>
        </dc:hasPart>
    </xsl:template>

    <xsl:template match="atom:entry[not(atom:content/@src)][parent::atom:feed]">
        <dc:hasPart>
            <xsl:call-template name="atom_entry"/>
        </dc:hasPart>
    </xsl:template>

    <xsl:template match="@* | node()" mode="copy">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()" mode="copy"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="rdf:RDF">
        <xsl:apply-templates/>
    </xsl:template>
    <xsl:template match="rdf:Description">
        <xsl:apply-templates select="*" mode="copy"/>
    </xsl:template>
    <xsl:template match="atom:id">
        <dc:identifier>
            <xsl:apply-templates/>
        </dc:identifier>
    </xsl:template>
    <xsl:template match="atom:updated">
        <dc:modified>
            <xsl:apply-templates/>
        </dc:modified>
    </xsl:template>
    <xsl:template match="atom:title">
        <dc:title>
            <xsl:apply-templates/>
        </dc:title>
    </xsl:template>
    <xsl:template match="atom:summary">
        <dc:abstract>
            <xsl:if test="@type='xhtml'">
                <xsl:attribute name="rdf:parseType">Literal</xsl:attribute>
            </xsl:if>
            <xsl:apply-templates mode="copy"/>
        </dc:abstract>
    </xsl:template>
    <!-- <xsl:template match="atom:generator">
        <dc:creator><xsl:apply-templates/></dc:creator>
    </xsl:template> -->
    <xsl:template match="atom:category">
        <dc:subject>
            <rdf:Description>
                <dcam:memberOf>
                    <xsl:value-of select="@scheme"/>
                </dcam:memberOf>
                <rdf:value>
                    <xsl:value-of select="@term"/>
                </rdf:value>
            </rdf:Description>
        </dc:subject>
    </xsl:template>
    <xsl:template match="atom:link[starts-with(@rel, 'http://')]">
        <xsl:variable name="rel-name" select="str:tokenize(@rel, '/')[last()]"/>
        <xsl:element name="{$rel-name}" namespace="{substring-before(@rel, $rel-name)}">
            <rdf:Description>
                <xsl:attribute name="rdf:about">
                    <xsl:value-of select="@href"/>
                </xsl:attribute>
            </rdf:Description>
        </xsl:element>
    </xsl:template>
    <xsl:template match="atom:link">
        <xsl:element name="rel:{@rel}">
            <xsl:attribute name="rdf:resource">
                <xsl:value-of select="@href"/>
            </xsl:attribute>
        </xsl:element>
    </xsl:template>
    <xsl:template match="atom:content">
        <xsl:element name="dc:format">
            <xsl:attribute name="rdf:datatype"
                >http://www.iana.org/assignments/media-types/</xsl:attribute>
            <xsl:value-of select="@type"/>
        </xsl:element>
    </xsl:template>

    <!-- Person -->
    <xsl:template mode="person_construct" match="atom:name">
        <foaf:name>
            <xsl:value-of select="."/>
        </foaf:name>
    </xsl:template>
    <xsl:template mode="person_construct" match="atom:uri">
        <foaf:homepage>
            <xsl:attribute name="rdf:resource">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </foaf:homepage>
    </xsl:template>
    <xsl:template mode="person_construct" match="atom:email">
        <foaf:mbox>
            <xsl:attribute name="rdf:resource">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </foaf:mbox>
    </xsl:template>
    <xsl:template match="atom:author[atom:name or atom:uri or atom:email]">
        <dc:creator>
            <foaf:Person>
                <xsl:attribute name="ID"
                    namespace="http://www.w3.org/1999/02/22-rdf-syntax-ns#">creator_<xsl:value-of
                        select="position()"/>
                </xsl:attribute>
                <xsl:apply-templates mode="person_construct"/>
            </foaf:Person>
        </dc:creator>
    </xsl:template>
    <xsl:template match="atom:contributor[atom:name or atom:uri or atom:email]">
        <dc:contributor>
            <foaf:Person>
                <xsl:apply-templates mode="person_construct"/>
            </foaf:Person>
        </dc:contributor>
    </xsl:template>
    <xsl:template match="*">
        <xsl:comment>Ignoring <xsl:value-of select="name()"/></xsl:comment>
    </xsl:template>
</xsl:stylesheet>
