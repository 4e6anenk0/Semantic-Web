<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <html>
        <body>
            <h2>Vacancies</h2>
            <table border="1">
                <tr bgcolor="blue">
                    <th>ID</th>
                    <th>Vacancy</th>
                    <th>Company name</th>
                    <th>Location</th>
                    <th>Description</th>
                    <th>Salary</th>
                    <th>Currency</th>
                </tr>
                <xsl:for-each select="vacancies/vacancy">
                    <tr>
                        <td>
                            <xsl:value-of select="@ID" />
                        </td>
                        <td>
                            <xsl:value-of select="name" />
                        </td>
                        <td>
                            <xsl:value-of select="company" />
                        </td>
                        <td>
                            <xsl:value-of select="location" />
                        </td>
                        <td>
                            <xsl:value-of select="description" />
                        </td>
                        <td>
                            <xsl:value-of select="salary_list/UAH" />
                            <br />
                            <xsl:value-of select="salary_list/USD" />
                            <br />
                            <xsl:value-of select="salary_list/EUR" />
                        </td>
                        <td>
                            <xsl:value-of select="salary_list/UAH/@curency" />
                            <br />
                            <xsl:value-of select="salary_list/USD/@curency" />
                            <br />
                            <xsl:value-of select="salary_list/EUR/@curency" />
                        </td>
                    </tr>
                </xsl:for-each>
            </table>
        </body>

        </html>
    </xsl:template>

</xsl:stylesheet>