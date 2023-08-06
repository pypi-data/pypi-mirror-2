<?xml version="1.0" encoding="UTF-8" ?>
<!--
Copies everything

@created 2009-06-30
@author Jukka Huhtamäki

-->

<xsl:stylesheet version="2.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    
    <xsl:output encoding="UTF-8" 
        indent="yes" 
        method="xml" />
    
    <xsl:template match="*|node()|@*">
        <xsl:copy>
            <xsl:apply-templates select="*|node()|@*"/>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>
