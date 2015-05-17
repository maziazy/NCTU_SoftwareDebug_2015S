<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
	<html>
	<head>
		<meta charset="utf-8" />
		<meta name="author" content="Maziazy" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge" />
		<title>Python Coverage Metrics</title>
		<link rel="stylesheet" type="text/css" href="css/main.css" />
		<script type="text/javascript" src="js/main.js"></script>
		<script type="text/javascript" src="js/sorttable.js"></script>
	</head>
	<body>
		<div id="banner">Python Coverage Metrics</div>
		<div id="wrapper">
			<div id="nav">
				<ul>
					<xsl:apply-templates select=".//class" mode="nav" />
					<li id="li-index" onclick="ChangePage('index');">Index</li>
				</ul>
			</div>
			<div id="content">
				<xsl:apply-templates select=".//class" mode="page" />
				<div class="page" id="page-index">
					Please select the class.<br/>
					You can click header cell of table to sort that column.<br/><br/>
					0 in Metrics 4 might means Infinity.<br/><br/>
					<table class="sortable">
						<thead>
							<tr>
								<th>Class name</th>
								<th title="Tarantula" width="100px">Significant Lines 1</th>
								<th title="The Ochiai similarity coefficient" width="100px">Significant Lines 2</th>
								<th title="The Ochiai similarity coefficient O^P" width="100px">Significant Lines 3</th>
								<th title="DStar" width="100px">Significant Lines 4</th>
							</tr>
						</thead>
						<tbody>
							<xsl:apply-templates select=".//class" mode="index" />
						</tbody>
						<tfoot>
						</tfoot>
					</table>
					<br/>
					Significant Lines 1: metrics 1 > 0.5<br/>
					Significant Lines 2: metrics 2 > mean (lazy)<br/>
					Significant Lines 3: metrics 3 > mean (lazy)<br/>
					Significant Lines 4: metrics 4 > mean (lazy)
				</div>
			</div>
		</div>
		<div id="footer">游力 Maziazy</div>
		<div id="Processing">Please wait for a while...</div>
	</body>
	</html>
</xsl:template>

<xsl:template match="class" mode="nav">
	<li>
		<xsl:attribute name="onclick">ChangePage('<xsl:value-of select="@name"/>')</xsl:attribute>
		<xsl:attribute name="id">li-<xsl:value-of select="@name"/></xsl:attribute>
		<xsl:value-of select="@name"/>
	</li>
</xsl:template>
<xsl:template match="class" mode="index">
	<tr>
		<td style="cursor:pointer;">
			<xsl:attribute name="onclick">ChangePage('<xsl:value-of select="@name"/>')</xsl:attribute>
			<xsl:value-of select="@name"/>
		</td>
		<xsl:variable name="m1-mean" select="0.5"/>
		<xsl:variable name="m2-mean" select="sum(.//line/@m2) div count(.//line[@m2!=0])"/>
		<xsl:variable name="m3-mean" select="sum(.//line/@m3) div count(.//line[@m3!=0])"/>
		<xsl:variable name="m4-mean" select="sum(.//line/@m4) div count(.//line[@m4!=0])"/>
		<td><xsl:value-of select="count(.//line[@m1 > $m1-mean])"/></td>
		<td><xsl:value-of select="count(.//line[@m2 > $m2-mean])"/></td>
		<td><xsl:value-of select="count(.//line[@m3 > $m3-mean])"/></td>
		<td><xsl:value-of select="count(.//line[@m4 > $m4-mean])"/></td>
	</tr>
</xsl:template>
<xsl:template match="class" mode="page">
	<div class="page">
		<xsl:attribute name="id">page-<xsl:value-of select="@name"/></xsl:attribute>
		<table class="sortable">
			<thead>
				<tr>
					<th>Line</th>
					<th>Success</th>
					<th>Fail</th>
					<th title="Tarantula" width="100px">Metric 1</th>
					<th title="The Ochiai similarity coefficient" width="100px">Metric 2</th>
					<th title="The Ochiai similarity coefficient O^P" width="100px">Metric 3</th>
					<th title="DStar" width="100px">Metric 4</th>
				</tr>
			</thead>
			<tbody>
				<xsl:apply-templates select=".//line" />
			</tbody>
			<tfoot>
			</tfoot>
		</table>
	</div>
</xsl:template>
<xsl:template match="line">
	<tr>
		<td><xsl:value-of select="@number"/></td>
		<td><xsl:value-of select="@s"/></td>
		<td><xsl:value-of select="@f"/></td>
		<td><xsl:value-of select="format-number(@m1, '0.00')"/></td>
		<td><xsl:value-of select="format-number(@m2, '0.00')"/></td>
		<td><xsl:value-of select="format-number(@m3, '0.00')"/></td>
		<td><xsl:value-of select="format-number(@m4, '0.00')"/></td>
	</tr>
</xsl:template>

</xsl:stylesheet>