<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">

    <xsl:output indent="yes" method="xml"/>
    
    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="Liste">
        <dimlex>
            <xsl:apply-templates/>
        </dimlex>
    </xsl:template>
    
    <xsl:template match="marqueur">
        <entry id="{@id}" word="{lemme[1]/text()}">
            <xsl:if test="nature='ambigu'">
                <ambiguity>
                    <non_conn>1</non_conn>
                    <sem_ambiguity>1</sem_ambiguity>
                </ambiguity>
            </xsl:if>
            <orths>
                <xsl:for-each select="lemme">
                    <orth type="{../@type}">
                        <xsl:value-of select="text()"/>
                    </orth>
                </xsl:for-each>
            </orths>
            <syn>
                <cat>
                    <xsl:value-of select="@cat"/>
                </cat>
                <xsl:for-each select="rel-EN">
                    <sem>
                        <arabic_relation sense="{text()}"/>
                    </sem>
                </xsl:for-each>
            </syn>
        </entry>
    </xsl:template>

</xsl:stylesheet>
