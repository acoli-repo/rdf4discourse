<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">

    <xsl:output indent="yes" method="xml"/>
    
    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="liste">
        <dimlex>
            <xsl:apply-templates/>
        </dimlex>
    </xsl:template>
    
    <xsl:template match="connecteur">
        <xsl:variable name="type" select="@type"/>
        <entry id="{@id}">
            <syn>
                <xsl:for-each select="@cat">
                    <cat>
                        <xsl:value-of select="."/>
                    </cat>
                </xsl:for-each>
                <xsl:for-each select="tokenize(@relations,',')">
                    <sem>
                        <sdrt_relation sense="{.}" type="{$type}"/>
                    </sem>
                </xsl:for-each>
            </syn>
            <orths>
                <xsl:for-each select="forme">
                    <orth>
                        <xsl:value-of select="normalize-space(.)"/>
                    </orth>
                </xsl:for-each>
            </orths>
            <xsl:for-each select="exemple">
                <example>
                    <xsl:apply-templates/>
                </example>
            </xsl:for-each>
            <xsl:for-each select="synonyme">
                <synonym connector="{@connecteur}"/>
            </xsl:for-each>            
        </entry>
    </xsl:template>
    
    <xsl:template match="text()">
        <xsl:value-of select="normalize-space(.)"/>
    </xsl:template>
</xsl:stylesheet>
