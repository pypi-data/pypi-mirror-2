<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml"></xsl:output>
  <xsl:template match="/icestats">
<load>
    <xsl:for-each select="source">
    <mount>
    <xsl:attribute name="name"><xsl:value-of select="@mount"></xsl:value-of></xsl:attribute>
    <xsl:value-of select="max_listeners - listeners"></xsl:value-of>
    </mount>
    </xsl:for-each>
</load>
  </xsl:template>
</xsl:stylesheet>
