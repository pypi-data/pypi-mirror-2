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

    <xsl:template match="atom:entry">
        <rdf:Description xml:lang="en" xml:base="{atom:id}">
            <xsl:attribute name="rdf:about">
                <xsl:value-of select="atom:id"/>
            </xsl:attribute>
            <xsl:element name="rdf:type">
                <xsl:attribute name="rdf:resource">
                    <xsl:value-of select="concat('http://www.w3.org/2005/Atom#', 'entry')"/>
                </xsl:attribute>
            </xsl:element>
            <xsl:apply-templates/>
        </rdf:Description>
    </xsl:template>

    <xsl:template match="atom:entry[atom:link[@rel='edit']]">
        <rdf:Description xml:lang="en" xml:base="{atom:link[@rel='edit']/@href}">
            <xsl:attribute name="rdf:about">
                <xsl:value-of select="atom:link[@rel='edit']/@href"/>
            </xsl:attribute>
            <xsl:element name="rdf:type">
                <xsl:attribute name="rdf:resource">
                    <xsl:value-of select="concat('http://www.w3.org/2005/Atom#', 'entry')"/>
                </xsl:attribute>
            </xsl:element>
            <xsl:apply-templates/>
        </rdf:Description>
    </xsl:template>

    <xsl:template match="atom:entry[parent::atom:feed]">
        <dc:hasPart>
            <rdf:Description xml:base="{atom:id}">
                <xsl:attribute name="rdf:about">
                    <xsl:value-of select="atom:id"/>
                </xsl:attribute>
                <xsl:element name="rdf:type">
                    <xsl:attribute name="rdf:resource">
                        <xsl:value-of select="concat('http://www.w3.org/2005/Atom#', 'entry')"/>
                    </xsl:attribute>
                </xsl:element>
                <xsl:apply-templates/>
            </rdf:Description>
        </dc:hasPart>
    </xsl:template>

    <xsl:template match="atom:entry[atom:link[@rel='edit']][parent::atom:feed]">
        <dc:hasPart>
            <rdf:Description xml:base="{atom:link[@rel='edit']/@href}">
                <xsl:attribute name="rdf:about">
                    <xsl:value-of select="atom:link[@rel='edit']/@href"/>
                </xsl:attribute>
                <xsl:element name="rdf:type">
                    <xsl:attribute name="rdf:resource">
                        <xsl:value-of select="concat('http://www.w3.org/2005/Atom#', 'entry')"/>
                    </xsl:attribute>
                </xsl:element>
                <xsl:apply-templates/>
            </rdf:Description>
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
                <xsl:choose>
                    <xsl:when test="atom:uri">
                        <xsl:attribute name="about"
                            namespace="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
                            <xsl:value-of select="atom:uri"/>
                        </xsl:attribute>
                    </xsl:when>
                    <xsl:when test="atom:email">
                        <xsl:attribute name="about"
                            namespace="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
                            <xsl:value-of select="atom:email"/>
                        </xsl:attribute>
                    </xsl:when>
                    <xsl:when test="atom:name">
                        <xsl:attribute name="ID"
                            namespace="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><xsl:value-of
                                select="atom:name"/>
                        </xsl:attribute>
                    </xsl:when>
                </xsl:choose>
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
