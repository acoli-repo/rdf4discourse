<?xml version="1.0" encoding="UTF-8" ?>

<!--
    Document   : lico2lemon.xsl
    Created on : 2017-11-05 10:09
    Author     : Christian Chiarcos
    Description:
        lossless rendering of DimLex in RDF (TTL)
        based on dimlex2lemon.xsl
-->

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output indent="no" method="text" encoding="utf-8"/>
    <xsl:strip-space elements="*"/>

    <xsl:param name="BASE">https://hlt-nlp.fbk.eu/technologies/lico#</xsl:param>

    <!-- returns the uri or the entry (short notation) -->
    <xsl:template name="entry-resource">
        <xsl:text>:</xsl:text>
        <xsl:for-each select="./ancestor-or-self::entry[1]">
            <xsl:value-of select="@id"/> 
            <!-- note that this yields numerical ids for lico -->
        </xsl:for-each>        
    </xsl:template>

    <xsl:template match="/">
        <xsl:text disable-output-escaping="yes">PREFIX dimlex: &lt;https://github.com/discourse-lab/dimlex/blob/master/DimLex.dtd#>
# LiCo is inspired by dimlex. As it does not provide a DTD or schema, we refer to the dimlex DTD, instead, even though there are differences.

PREFIX dimlex_data: &lt;https://github.com/discourse-lab/dimlex/blob/master/DimLex.xml#>
# explicit cross-references with DimLex as given in entry/commento

PREFIX pdtb3: &lt;https://raw.githubusercontent.com/discourse-lab/dimlex/master/inventory-pdtb3-senses.txt#> # preliminary, there is no official documentation yet
PREFIX ontolex: &lt;http://www.w3.org/ns/lemon/ontolex#>
PREFIX synsem: &lt;http://www.w3.org/ns/lemon/synsem#>
PREFIX decomp: &lt;http://www.w3.org/ns/lemon/decomp#>
PREFIX vartrans: &lt;http://www.w3.org/ns/lemon/vartrans#>
PREFIX lime: &lt;http://www.w3.org/ns/lemon/lime#>
PREFIX rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: &lt;http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: &lt;http://www.w3.org/2004/02/skos/core#>
PREFIX xml: &lt;http://www.w3.org/TR/xml/#>
PREFIX : &lt;</xsl:text>
        <xsl:value-of select="$BASE"/>
        <xsl:text disable-output-escaping="yes">>&#10;&#10;</xsl:text>
        <xsl:apply-templates/>
    </xsl:template>
    
    <xsl:template match="lico|dimlex|orths">
        <xsl:apply-templates/>
    </xsl:template>
    
    <xsl:template match="orth">
        <xsl:text>;&#10;</xsl:text>
        <xsl:call-template name="get-indent"/>
        <xsl:text>ontolex:</xsl:text>
        <xsl:choose>
            <xsl:when test="@canonical='1'">canonical</xsl:when>
            <xsl:when test="@canonical='0'">other</xsl:when>
            <xsl:otherwise>lexical</xsl:otherwise>
        </xsl:choose>
        <xsl:text>Form [ ontolex:writtenRep "</xsl:text>
        <xsl:value-of select="string-join(part/text(),' ')"/>
        <xsl:text>"@it</xsl:text>
        <xsl:for-each select="@*|part/@*">
            <xsl:if test="name()!='canonical'">
                <xsl:text>; dimlex:</xsl:text>
                <xsl:value-of select="name()"/>
                <xsl:text> "</xsl:text>
                <xsl:value-of select="."/>
                <xsl:text>"</xsl:text>
            </xsl:if>
        </xsl:for-each>
        <xsl:text>]</xsl:text>
    </xsl:template>
    
    <xsl:template match="entry">
        <xsl:call-template name="get-indent"/>
        <xsl:call-template name="entry-resource"/>
        <xsl:text> a ontolex:LexicalEntry</xsl:text>
        <xsl:apply-templates/>
        <xsl:text>.&#10;&#10;</xsl:text>
    </xsl:template>
    
    <!-- in LICO 1.0, all commento elements are cross-references to dimlex -->
    <xsl:template match="commento">
      <xsl:if test="normalize-space(string-join(text(),' '))!=''">        
        <xsl:if test="exists(./preceding-sibling::*[exists(.//text()) or exists(./descendant-or-self::*/@*)])">
            <xsl:text>;</xsl:text>
        </xsl:if>
        <xsl:text>&#10;</xsl:text>
        <xsl:call-template name="get-indent"/>
        <xsl:choose>
            <xsl:when test="starts-with(text(),'DimLex.xml/id=')">
                <xsl:text>vartrans:translatableAs dimlex_data:</xsl:text>
                <xsl:value-of select="replace(text(),'.*=&quot;([^&quot;]+)&quot;.*','$1')"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>rdfs:comment "</xsl:text>
                <xsl:value-of select="replace(normalize-space(string-join(text(),' ')),'&quot;','\\&quot;')"/>
                <xsl:text>"</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
      </xsl:if>
    </xsl:template>

    <!-- instead of dimlex:pdtb3_relation, namming conventions adapted to DimLex -->
    <xsl:template match="coh-relation">
      <xsl:if test="exists(./text()[normalize-space(.)!=''])">
        <xsl:if test="exists(./preceding-sibling::*[exists(.//text()) or exists(./descendant-or-self::*/@*)])">
            <xsl:text>;</xsl:text>
        </xsl:if>
        <xsl:text>&#10;</xsl:text>
        <xsl:call-template name="get-indent"/>
        <xsl:text>a ontolex:LexicalSense; ontolex:isSenseOf </xsl:text>
        <xsl:call-template name="entry-resource"/>
        <xsl:text>; ontolex:isLexicalizedSenseOf pdtb3:</xsl:text>
        <xsl:value-of select="
            replace(
            replace(
            replace(
            lower-case(replace(string-join(text(),''),'\(.*','')),
            ' ',''),
            '.*:([^a]|a[^r]|ar[^g]|arg[^0-9])','$1'),
            '[: ]+','-')"/>
      </xsl:if>
    </xsl:template>
    
    <xsl:template name="get-indent">
        <xsl:value-of select="replace(string-join(./ancestor-or-self::*/name(),'  '),'[^ ]','')"/>
    </xsl:template>
    
    <!-- this is a generic XML converter, it does require a root URI as subject  -->    
    <xsl:template match="*">
      <xsl:if test="exists(.//text()) or exists(./descendant-or-self::*/@*)">
          <xsl:if test="exists(./preceding-sibling::*[exists(.//text()) or exists(./descendant-or-self::*/@*)])">
            <xsl:text>;</xsl:text>
        </xsl:if>
        <xsl:text>&#10;</xsl:text>
        <xsl:call-template name="get-indent"/>
        <xsl:text>dimlex:</xsl:text>
        <xsl:value-of select="name()"/>
        <xsl:choose>
            <xsl:when test="not(exists(*)) and not(exists(@*))">
                <xsl:text> "</xsl:text>
                <xsl:value-of select="string-join(text(),' ')"/>
                <xsl:text>"</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text> [ </xsl:text>
                <xsl:apply-templates/>
                <xsl:if test="exists(text())">
                    <xsl:if test="exists(*)">
                        <xsl:text>;&#10;</xsl:text>
                        <xsl:call-template name="get-indent"/>
                    </xsl:if>
                    <xsl:text>xml:CDATA "</xsl:text>
                    <xsl:value-of select="replace(replace(string-join(text(),' '),'&quot;','\\&quot;'),'[ \t\r\n]+',' ')"/>
                    <xsl:text>"</xsl:text>
                </xsl:if>
                <xsl:for-each select="@*">
                    <xsl:if test="position()>1 or exists(../text()) or exists(../*[exists(.//text()) or exists(./descendant-or-self::*/@*)])">
                        <xsl:text>;</xsl:text>
                    </xsl:if>
                    <xsl:text> dimlex:</xsl:text>
                    <xsl:value-of select="name()"/>
                    <xsl:text> "</xsl:text>
                    <xsl:value-of select="."/>
                    <xsl:text>"</xsl:text>
                </xsl:for-each>
                <xsl:text> ]</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
      </xsl:if>
    </xsl:template>
    
    <xsl:template match="text()"/>

</xsl:stylesheet> 
