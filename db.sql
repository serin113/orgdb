-- Created in 2019-01-31 for PSYSC as part of a system for managing science club affiliations.

-- Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
-- Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

-- Code History:
-- 2019/02/06 (Nathan) - Initial working code and documentation
-- 2019/02/17 (Simon) - Cleanup to follow same format as the mysqldump output
-- 2019/02/27 (Nathan) - Added table for affiliation application

-- MySQL dump 10.13  Distrib 8.0.14, for Win64 (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version 8.0.14

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `affiliationapplication`
--

DROP TABLE IF EXISTS `affiliationapplication`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `affiliationapplication` (
  `appID` smallint(6) NOT NULL,
  `hasRecord` tinyint(4) DEFAULT NULL,
  `clubID` varchar(45) DEFAULT NULL,
  `dateCreated` date NOT NULL,
  `region` varchar(10) DEFAULT NULL,
  `level` tinyint(4) DEFAULT NULL,
  `type` tinyint(4) DEFAULT NULL,
  `school` varchar(200) DEFAULT NULL,
  `clubName` varchar(200) DEFAULT NULL,
  `address` varchar(500) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `adviserName` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `schoolYear` year(4) DEFAULT NULL,
  `yearsAffiliated` int(11) DEFAULT NULL,
  `SCA` smallint(10) DEFAULT NULL,
  `SCM` smallint(10) DEFAULT NULL,
  `paymentMode` varchar(100) DEFAULT NULL,
  `paymentDate` date DEFAULT NULL,
  `paymentID` varchar(200) DEFAULT NULL,
  `paymentAmount` int(11) DEFAULT NULL,
  `receiptNumber` varchar(200) DEFAULT NULL,
  `paymentSendMode` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`appID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `affiliationapplication`
--

LOCK TABLES `affiliationapplication` WRITE;
/*!40000 ALTER TABLE `affiliationapplication` DISABLE KEYS */;
/*!40000 ALTER TABLE `affiliationapplication` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `affiliationrecordstable`
--

DROP TABLE IF EXISTS `affiliationrecordstable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `affiliationrecordstable` (
  `clubID` varchar(50) NOT NULL,
  `dateUpdated` date NOT NULL,
  `region` varchar(10) DEFAULT NULL,
  `level` tinyint(1) DEFAULT NULL,
  `type` tinyint(1) DEFAULT NULL,
  `school` varchar(100) DEFAULT NULL,
  `clubName` varchar(100) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `province` varchar(45) DEFAULT NULL,
  `adviserName` varchar(100) DEFAULT NULL,
  `contact` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`clubID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `affiliationrecordstable`
--

LOCK TABLES `affiliationrecordstable` WRITE;
/*!40000 ALTER TABLE `affiliationrecordstable` DISABLE KEYS */;
INSERT INTO `affiliationrecordstable` VALUES ('2eb87bd9-1a35-4c14-9ab6-43dd26aff2e5','2019-02-20','1',1,1,'aasdaa','aasbbvv','#6 Guyabano Street, Zone 1, North Signal Village','Taguig','asjda',';sjd','094999494912','roy.nathan99@yahoo.com'),('4d2d239f-717f-4943-a89f-c31bb64e1670','2019-02-20','1',1,1,'aaaa','aaaa','#6 Guyabano Street, Zone 1, North Signal Village','Taguig','asjda',';sjd','094999494912','roy.nathan99@yahoo.com'),('fbe329b2-00b9-4bea-b911-919465ffda1e','2019-02-20','1',1,1,'aasdaa','aasbb','#6 Guyabano Street, Zone 1, North Signal Village','Taguig','asjda',';sjd','094999494912','roy.nathan99@yahoo.com');
/*!40000 ALTER TABLE `affiliationrecordstable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `affiliationtable`
--

DROP TABLE IF EXISTS `affiliationtable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `affiliationtable` (
  `affiliationID` varchar(50) NOT NULL,
  `affiliated` tinyint(1) NOT NULL,
  `status` varchar(45) DEFAULT NULL,
  `hasAffiliationForms` tinyint(1) DEFAULT NULL,
  `benefits` varchar(200) DEFAULT NULL,
  `remarks` varchar(200) DEFAULT NULL,
  `schoolYear` year(4) DEFAULT NULL,
  `yearsAffiliated` int(11) DEFAULT NULL,
  `SCA` smallint(10) DEFAULT NULL,
  `SCM` smallint(10) DEFAULT NULL,
  `paymentMode` varchar(200) DEFAULT NULL,
  `paymentDate` date DEFAULT NULL,
  `paymentID` varchar(200) DEFAULT NULL,
  `paymentAmount` int(11) DEFAULT NULL,
  `receiptNumber` varchar(200) DEFAULT NULL,
  `paymentSendMode` varchar(200) DEFAULT NULL,
  `AffiliationRecordsTable_clubID` varchar(50) NOT NULL,
  PRIMARY KEY (`affiliationID`,`AffiliationRecordsTable_clubID`),
  KEY `fk_AffiliationTable_AffiliationRecordsTable_idx` (`AffiliationRecordsTable_clubID`),
  CONSTRAINT `fk_AffiliationTable_AffiliationRecordsTable` FOREIGN KEY (`AffiliationRecordsTable_clubID`) REFERENCES `affiliationrecordstable` (`clubID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `affiliationtable`
--

LOCK TABLES `affiliationtable` WRITE;
/*!40000 ALTER TABLE `affiliationtable` DISABLE KEYS */;
INSERT INTO `affiliationtable` VALUES ('536379c3-e1ed-4214-ae24-785c9be04e64',1,'jklas',1,'wld','lkdjf',2019,2,29,21,'912038','2019-02-20','jwfqwoje',1928,'821','834729','fbe329b2-00b9-4bea-b911-919465ffda1e'),('9798089b-c4a5-4c2b-94a0-e48be4326fd0',1,'jklas',1,'wld','lkdjf',2019,2,29,21,'912038','2019-02-20','jwfqwoje',1928,'821','834729','2eb87bd9-1a35-4c14-9ab6-43dd26aff2e5'),('992ee708-9819-427d-bd45-7be0dbfbae33',1,'jklas',1,'wld','lkdjf',2019,2,29,21,'912038','2019-02-20','jwfqwoje',1928,'821','834729','4d2d239f-717f-4943-a89f-c31bb64e1670');
/*!40000 ALTER TABLE `affiliationtable` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-27 13:51:10
