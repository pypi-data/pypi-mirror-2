<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:dv="http://namespaces.plone.org/xdv"
    xmlns:dyn="http://exslt.org/dynamic"
    xmlns:esi="http://www.edge-delivery.org/esi/1.0"
    xmlns:exsl="http://exslt.org/common"
    xmlns:set="http://exslt.org/sets"
    xmlns:str="http://exslt.org/strings"
    xmlns:xhtml="http://www.w3.org/1999/xhtml"
    xmlns:xml="http://www.w3.org/XML/1998/namespace"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    exclude-result-prefixes="dv dyn exsl xml">

    <xsl:param name="defaultsurl">defaults.xsl</xsl:param>
    <xsl:param name="usebase"/>
    <xsl:variable name="rules" select="//dv:*[@theme]"/>
    <xsl:variable name="drop-content-rules" select="//dv:drop[@content]"/>
    <xsl:variable name="inline-xsl" select="/dv:rules/xsl:*"/>
    <xsl:variable name="themes" select="//dv:theme"/>
    <xsl:variable name="conditional" select="//dv:theme[@merged-condition]"/>
    <xsl:variable name="unconditional" select="//dv:theme[not(@merged-condition)]"/>
    <xsl:variable name="defaults" select="document($defaultsurl)"/>

    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="/">
        <xsl:apply-templates select="$defaults/xsl:stylesheet"/>
    </xsl:template>

    <!--
        Boilerplate
    -->

    <xsl:template match="xsl:stylesheet">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:if test="$rules[@method='document']">
                <xsl:choose>
                    <xsl:when test="$usebase">
                        <!-- When usebase is true, document() includes are resolved internally using the base tag -->
                        <xsl:text>&#10;    </xsl:text>
                        <xsl:element name="xsl:variable">
                            <xsl:attribute name="name">base</xsl:attribute>
                            <xsl:text>/</xsl:text>
                        </xsl:element>
                        <xsl:text>&#10;</xsl:text>
                    </xsl:when>
                    <xsl:otherwise>
                        <!-- otherwise use a hack to ensure the relative path is used -->
                        <xsl:text>&#10;    </xsl:text>
                        <xsl:element name="xsl:variable">
                            <xsl:attribute name="name">base-rtf</xsl:attribute>
                        </xsl:element>
                        <xsl:text>&#10;</xsl:text>
                        <xsl:text>&#10;    </xsl:text>
                        <xsl:element name="xsl:variable">
                            <xsl:attribute name="name">base</xsl:attribute>
                            <xsl:attribute name="select">exsl:node-set($base-rtf)</xsl:attribute>
                        </xsl:element>
                        <xsl:text>&#10;</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:if>
            <xsl:apply-templates select="node()"/>
            <xsl:text>&#10;    </xsl:text>
            <xsl:element name="xsl:template">
                <xsl:attribute name="match">/</xsl:attribute>
                <xsl:choose>
                    <xsl:when test="$conditional">
                        <xsl:element name="xsl:choose">
                            <xsl:for-each select="$conditional">
                                <xsl:variable name="themeid" select="@xml:id"/>
                                <xsl:text>&#10;</xsl:text>
                                <xsl:element name="xsl:when">
                                    <xsl:attribute name="test">
                                        <xsl:value-of select="@merged-condition"/>
                                    </xsl:attribute>
                                    <xsl:element name="xsl:apply-templates">
                                        <xsl:attribute name="select">.</xsl:attribute>
                                        <xsl:attribute name="mode">
                                            <xsl:value-of select="$themeid"/>
                                        </xsl:attribute>
                                    </xsl:element>
                                </xsl:element>
                                <xsl:text>&#10;</xsl:text>
                            </xsl:for-each>
                            <xsl:text>&#10;</xsl:text>
                            <xsl:element name="xsl:otherwise">
                                <xsl:element name="xsl:apply-templates">
                                    <xsl:attribute name="select">@*|node()</xsl:attribute>
                                    <xsl:if test="$unconditional">
                                        <xsl:for-each select="$unconditional">
                                            <xsl:variable name="themeid" select="@xml:id"/>
                                            <xsl:attribute name="mode">
                                                <xsl:value-of select="$themeid"/>
                                            </xsl:attribute>
                                        </xsl:for-each>
                                    </xsl:if>
                                </xsl:element>
                            </xsl:element>
                            <xsl:text>&#10;</xsl:text>
                        </xsl:element>
                    </xsl:when>
                    <xsl:when test="$unconditional"> <!-- assert unconditional = 1 -->
                        <xsl:for-each select="$unconditional">
                            <xsl:variable name="themeid" select="@xml:id"/>
                            <xsl:element name="xsl:apply-templates">
                                <xsl:attribute name="select">.</xsl:attribute>
                                <xsl:attribute name="mode">
                                    <xsl:value-of select="$themeid"/>
                                </xsl:attribute>
                            </xsl:element>
                        </xsl:for-each>
                    </xsl:when>
                </xsl:choose>
            </xsl:element>
            <xsl:text>&#10;</xsl:text>
            <xsl:for-each select="$themes">
                <xsl:variable name="themeid" select="@xml:id"/>
                <xsl:text>&#10;    </xsl:text>
                <xsl:comment>THEME <xsl:value-of select="$themeid"/>: <xsl:choose>
                        <xsl:when test="@href"><xsl:value-of select="@href"/></xsl:when>
                        <xsl:otherwise>(inline)</xsl:otherwise>
                    </xsl:choose>
                </xsl:comment>
                <xsl:text>&#10;</xsl:text>
                <!-- If there are any <drop @content> rules, put it in 
                here. -->
                <xsl:for-each select="$drop-content-rules">
                    <xsl:text>&#10;    </xsl:text>
                    <xsl:element name="xsl:template">
                        <xsl:attribute name="match">
                            <xsl:value-of select="@content"/>
                        </xsl:attribute>
                        <xsl:attribute name="mode">
                            <xsl:value-of select="$themeid"/>
                        </xsl:attribute>
                        <xsl:comment>Do nothing, skip these nodes</xsl:comment>
                    </xsl:element>
                    <xsl:text>&#10;</xsl:text>
                </xsl:for-each>
                <!-- template for this theme -->
                <xsl:text>&#10;    </xsl:text>
                <xsl:element name="xsl:template">
                    <xsl:attribute name="match">/</xsl:attribute>
                    <xsl:attribute name="mode">
                        <xsl:value-of select="$themeid"/>
                    </xsl:attribute>
                    <xsl:apply-templates select="./*" mode="rewrite-mode">
                        <xsl:with-param name="mode" select="$themeid"/>
                    </xsl:apply-templates>
                </xsl:element>
                <xsl:text>&#10;</xsl:text>
                <!-- Copy the default templates into this theme's mode -->
                <xsl:for-each select="$defaults/xsl:stylesheet/xsl:template[not(@mode)] | $inline-xsl[local-name()='template' and not(@mode)]">
                    <xsl:text>&#10;    </xsl:text>
                    <xsl:apply-templates select="." mode="rewrite-mode">
                        <xsl:with-param name="mode" select="$themeid"/>
                    </xsl:apply-templates>
                    <xsl:text>&#10;</xsl:text>
                </xsl:for-each>
            </xsl:for-each>
            <!-- Copy the inline xsl from rules (usually xsl:output) -->
            <xsl:for-each select="$inline-xsl[not(local-name()='template' and @mode)]">
                <xsl:text>&#10;    </xsl:text>
                <xsl:copy-of select="."/>
                <xsl:text>&#10;</xsl:text>
            </xsl:for-each>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="@*|node()" mode="rewrite-mode">
        <xsl:param name="mode"/>
        <xsl:copy>
            <xsl:apply-templates select="@*|node()" mode="rewrite-mode">
                <xsl:with-param name="mode" select="$mode"/>
            </xsl:apply-templates>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="xsl:template[not(@mode)] | xsl:apply-templates[not(@mode)]" mode="rewrite-mode">
        <xsl:param name="mode"/>
        <xsl:copy>
            <xsl:attribute name="mode">
                <xsl:value-of select="$mode"/>
            </xsl:attribute>
            <xsl:apply-templates select="@*|node()" mode="rewrite-mode">
                <xsl:with-param name="mode" select="$mode"/>
            </xsl:apply-templates>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="xsl:stylesheet/@exclude-result-prefixes">
        <xsl:choose>
            <xsl:when test="$rules[@method='esi']">
                <xsl:copy/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:attribute name="exclude-result-prefixes"><xsl:value-of select="."/> esi</xsl:attribute>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
