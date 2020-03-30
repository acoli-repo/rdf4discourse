<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output indent="yes" method="xml" encoding="utf-8"/>

    <xsl:param name="BASE">https://github.com/discourse-lab/dimlex/blob/master/DimLex.xml#</xsl:param>

    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="*[name()='czedlex']">
        <dimlex>
            <xsl:for-each select="@*">
                <xsl:copy/>
            </xsl:for-each>
            <xsl:apply-templates/>
        </dimlex>
    </xsl:template>
    
    <xsl:template match="*[name()='lemma']">
        <entry>
            <xsl:for-each select="@*">
                <xsl:copy/>
            </xsl:for-each>
            <orths>
                <orth canonical="1">
                    <xsl:for-each select="*[name()='text']">
                        <part type="{../*[name()='type'][1]/text()[1]}">
                            <xsl:value-of select="."/>
                        </part>
                    </xsl:for-each>
                </orth>
            </orths>
            <xsl:for-each select="*[count(@*)&gt;0 or count(text())&gt;0]">
                <xsl:copy>
                    <xsl:for-each select="@*">
                        <xsl:copy/>
                    </xsl:for-each>
                </xsl:copy>
                <xsl:for-each select="./text()">
                    <xsl:copy/>
                </xsl:for-each>                                
            </xsl:for-each>
            <xsl:for-each select="*[name()='usages']/*[name()='conn-usages']/*[name()='usage']">
                <syn>
                    <xsl:if test="count(*[name()='pos'][1])=1">
                    <cat>
                        <xsl:for-each select="*[name()='pos']/text()">
							<xsl:value-of select="."/>
							</xsl:for-each>
                    </cat>
                    </xsl:if>
                    <xsl:for-each select="*[name()='sense']">
                        <sem>
                            <pdt_relation sense="{text()}" freq="{../@pdt_count}">
                                <xsl:for-each select="../*[name()='pdt']">
                                    <xsl:copy>
                                        <xsl:for-each select="@*">
                                            <xsl:copy/>
                                        </xsl:for-each>
                                        <xsl:apply-templates/>
                                    </xsl:copy>
                                </xsl:for-each>
                            </pdt_relation>
                            <xsl:for-each select="*[count(@*)&gt;0 or count(text())&gt;0]">
                                <xsl:copy>
                                    <xsl:for-each select="@*">
                                        <xsl:copy/>
                                    </xsl:for-each>
                                </xsl:copy>
                                <xsl:for-each select="./text()">
                                    <xsl:copy/>
                                </xsl:for-each>                                
                            </xsl:for-each>
                            
                            <examples>
                                <xsl:for-each select="*[name()='examples']/*[name()='example']">
                                    <xsl:apply-templates/>
                                </xsl:for-each>
                            </examples>
                        </sem>
                    </xsl:for-each>
                </syn>
            </xsl:for-each>
        </entry>
        
        <xsl:for-each select=".//*[name()='complex_form']">
            <entry id="{concat(./ancestor::*[name()='usage'][1]/@id,'_',
                count(./preceding-sibling::*[name()='complex_form']))}">
                <xsl:for-each select="@*">
                    <xsl:copy/>
                </xsl:for-each>
                <orths>
                    <orth>
                        <xsl:for-each select="*[name()='text']">
                            <part type="complex_form">
                                <xsl:value-of select="."/>
                            </part>
                        </xsl:for-each>                    
                    </orth>
                </orths>
                <syn>
                    <cat>
                        <xsl:for-each select="../../*[name()='pos'][1]">
                            <xsl:for-each select="@*">
                                <xsl:copy/>
                            </xsl:for-each>
                            <xsl:apply-templates/>
                        </xsl:for-each>
                    </cat>
                    <xsl:for-each select="../../*[name()='sense']">
                        <sem>
                            <pdt_relation sense="{text()}"/>
                            <xsl:for-each select="*[count(@*)&gt;0 or count(text())&gt;0]">
                                <xsl:copy>
                                    <xsl:for-each select="@*">
                                        <xsl:copy/>
                                    </xsl:for-each>
                                </xsl:copy>
                                <xsl:for-each select="./text()">
                                    <xsl:copy/>
                                </xsl:for-each>                                
                            </xsl:for-each>
                        </sem>
                    </xsl:for-each>
                </syn>
            </entry>
        </xsl:for-each>
    </xsl:template>
    
    <xsl:template match="*">
        <xsl:if test="name()!='head'">
            <xsl:copy>
                <xsl:for-each select="@*">
                    <xsl:copy/>
                </xsl:for-each>
                <xsl:apply-templates/>
            </xsl:copy>
        </xsl:if>
    </xsl:template>

</xsl:stylesheet> 
