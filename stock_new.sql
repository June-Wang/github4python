-- MySQL dump 10.13  Distrib 5.5.47, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: stock
-- ------------------------------------------------------
-- Server version	5.5.47-0+deb8u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cashflow`
--

DROP TABLE IF EXISTS `cashflow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cashflow` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` char(6),
  `name` varchar(20),
  `cf_sales` double DEFAULT NULL,
  `rateofreturn` double DEFAULT NULL,
  `cf_nm` double DEFAULT NULL,
  `cf_liabilities` double DEFAULT NULL,
  `cashflowratio` double DEFAULT NULL,
  `year` year(4) DEFAULT NULL,
  `season` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_name_year_season` (`code`,`name`,`year`,`season`)
) ENGINE=InnoDB AUTO_INCREMENT=42606 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `debtpaying`
--

DROP TABLE IF EXISTS `debtpaying`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `debtpaying` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` char(6),
  `name` varchar(20),
  `currentratio` text,
  `quickratio` text,
  `cashratio` text,
  `icratio` text,
  `sheqratio` text,
  `adratio` text,
  `year` year(4) DEFAULT NULL,
  `season` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_name_year_season` (`code`,`name`,`year`,`season`)
) ENGINE=InnoDB AUTO_INCREMENT=42606 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `growth`
--

DROP TABLE IF EXISTS `growth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `growth` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` char(6),
  `name` varchar(20),
  `mbrg` double DEFAULT NULL,
  `nprg` double DEFAULT NULL,
  `nav` double DEFAULT NULL,
  `targ` double DEFAULT NULL,
  `epsg` double DEFAULT NULL,
  `seg` double DEFAULT NULL,
  `year` year(4) DEFAULT NULL,
  `season` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_name_year_season` (`code`,`name`,`year`,`season`)
) ENGINE=InnoDB AUTO_INCREMENT=41008 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `list`
--

DROP TABLE IF EXISTS `list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `list` (
  `code` char(6),
  `name` varchar(20),
  `industry` varchar(20),
  `area` varchar(10),
  `pe` double DEFAULT NULL,
  `outstanding` double DEFAULT NULL,
  `totals` double DEFAULT NULL,
  `totalAssets` double DEFAULT NULL,
  `liquidAssets` double DEFAULT NULL,
  `fixedAssets` double DEFAULT NULL,
  `reserved` double DEFAULT NULL,
  `reservedPerShare` double DEFAULT NULL,
  `esp` double DEFAULT NULL,
  `bvps` double DEFAULT NULL,
  `pb` double DEFAULT NULL,
  `timeToMarket` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`code`),
  UNIQUE KEY `code_name` (`code`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `operation`
--

DROP TABLE IF EXISTS `operation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `operation` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` char(6),
  `name` varchar(20),
  `arturnover` double DEFAULT NULL,
  `arturndays` double DEFAULT NULL,
  `inventory_turnover` double DEFAULT NULL,
  `inventory_days` double DEFAULT NULL,
  `currentasset_turnover` double DEFAULT NULL,
  `currentasset_days` double DEFAULT NULL,
  `year` year(4) DEFAULT NULL,
  `season` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_name_year_season` (`code`,`name`,`year`,`season`)
) ENGINE=InnoDB AUTO_INCREMENT=42606 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `profit`
--

DROP TABLE IF EXISTS `profit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `profit` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` char(6),
  `name` varchar(20),
  `roe` double DEFAULT NULL,
  `net_profit_ratio` double DEFAULT NULL,
  `gross_profit_rate` double DEFAULT NULL,
  `net_profits` double DEFAULT NULL,
  `eps` double DEFAULT NULL,
  `business_income` double DEFAULT NULL,
  `bips` double DEFAULT NULL,
  `year` year(4) DEFAULT NULL,
  `season` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_name_year_season` (`code`,`name`,`year`,`season`)
) ENGINE=InnoDB AUTO_INCREMENT=43164 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `report`
--

DROP TABLE IF EXISTS `report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `report` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` char(6),
  `name` varchar(20),
  `eps` double DEFAULT NULL,
  `eps_yoy` double DEFAULT NULL,
  `bvps` double DEFAULT NULL,
  `roe` double DEFAULT NULL,
  `epcf` double DEFAULT NULL,
  `net_profits` double DEFAULT NULL,
  `profits_yoy` double DEFAULT NULL,
  `distrib` double DEFAULT NULL,
  `report_date` text,
  `year` year(4) DEFAULT NULL,
  `season` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_name_year_season` (`code`,`name`,`year`,`season`)
) ENGINE=InnoDB AUTO_INCREMENT=42461 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-04-21 21:49:22
