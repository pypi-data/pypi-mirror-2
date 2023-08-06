<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
    xmlns:svg="http://www.w3.org/Graphics/SVG/SVG-19990812.dtd"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output indent="yes" media-type="image/svg" method="xml" />
    <xsl:template match="/">
        <svg height="3in" width="3in">
            <g style="stroke: #000000">
                <!-- draw the axes -->
                <line x1="0" x2="150" y1="150" y2="150" />
                <line x1="0" x2="0" y1="0" y2="150" />
                <text x="0" y="10">Revenue</text>
                <text x="150" y="165">Division</text>
                <xsl:for-each select="sales/division">
                    <!-- define some useful variables -->
                    <!-- the bar's x position -->
                    <xsl:variable name="pos" select="(position()*40)-30" />
                    <!-- the bar's height -->
                    <xsl:variable name="height" select="revenue*10" />
                    <!-- the rectangle -->
                    <rect height="{$height}" width="20" x="{$pos}"
                        y="{150-$height}" />
                    <!-- the text label -->
                    <text x="{$pos}" y="165">
                        <xsl:value-of select="@id" />
                    </text>
                    <!-- the bar value -->
                    <text x="{$pos}" y="{145-$height}">
                        <xsl:value-of select="revenue" />
                    </text>
                </xsl:for-each>
            </g>
        </svg>
    </xsl:template>
</xsl:stylesheet>
