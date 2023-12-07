CREATE DATABASE  IF NOT EXISTS `jobmatch` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `jobmatch`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: jobmatchserver.mariadb.database.azure.com    Database: jobmatch
-- ------------------------------------------------------
-- Server version	5.6.47.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `AdminID` int(11) NOT NULL AUTO_INCREMENT,
  `Username` varchar(255) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`AdminID`),
  UNIQUE KEY `Username_UNIQUE` (`Username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auditlog`
--

DROP TABLE IF EXISTS `auditlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auditlog` (
  `LogID` int(11) NOT NULL AUTO_INCREMENT,
  `UserID` int(11) NOT NULL,
  `ActionType` varchar(255) NOT NULL,
  `Details` text DEFAULT NULL,
  `Timestamp` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`LogID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `company`
--

DROP TABLE IF EXISTS `company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company` (
  `CompanyID` int(11) NOT NULL AUTO_INCREMENT,
  `Username` varchar(255) DEFAULT NULL,
  `CompanyName` varchar(255) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Description` text DEFAULT NULL,
  `Location` varchar(255) DEFAULT NULL,
  `PictureURL` varchar(255) DEFAULT NULL,
  `Contact` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `VerificationToken` varchar(255) DEFAULT NULL,
  `EmailVerified` tinyint(1) DEFAULT 0,
  `is_blocked` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`CompanyID`),
  UNIQUE KEY `Username_UNIQUE` (`Username`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `companyad`
--

DROP TABLE IF EXISTS `companyad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `companyad` (
  `CompanyAdID` int(11) NOT NULL AUTO_INCREMENT,
  `ProfessionalID` int(11) DEFAULT NULL,
  `BottomSalary` int(11) DEFAULT NULL,
  `TopSalary` int(11) DEFAULT NULL,
  `MotivationDescription` text DEFAULT NULL,
  `Location` varchar(255) DEFAULT NULL,
  `Status` enum('Active','Archived') NOT NULL DEFAULT 'Active',
  `CompanyAdRequirement` text DEFAULT NULL,
  `CreatedAt` timestamp NULL DEFAULT current_timestamp(),
  `UpdatedAt` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`CompanyAdID`),
  KEY `ProfessionalID_idx` (`ProfessionalID`),
  KEY `idx_status_on_companyad` (`Status`),
  KEY `idx_location_on_companyad` (`Location`),
  CONSTRAINT `companyad_ibfk_1` FOREIGN KEY (`ProfessionalID`) REFERENCES `professional` (`ProfessionalID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `companyadskill`
--

DROP TABLE IF EXISTS `companyadskill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `companyadskill` (
  `CompanyAdID` int(11) NOT NULL,
  `SkillID` int(11) NOT NULL,
  `Level` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`CompanyAdID`,`SkillID`),
  KEY `fk_CompanyAdID_idx` (`CompanyAdID`),
  KEY `fk_SkillID_idx` (`SkillID`),
  CONSTRAINT `companyadskill_ibfk_1` FOREIGN KEY (`CompanyAdID`) REFERENCES `companyad` (`CompanyAdID`),
  CONSTRAINT `companyadskill_ibfk_2` FOREIGN KEY (`SkillID`) REFERENCES `skill` (`SkillID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jobad`
--

DROP TABLE IF EXISTS `jobad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobad` (
  `JobAdID` int(11) NOT NULL AUTO_INCREMENT,
  `CompanyID` int(11) DEFAULT NULL,
  `BottomSalary` int(11) DEFAULT NULL,
  `TopSalary` int(11) DEFAULT NULL,
  `JobDescription` text DEFAULT NULL,
  `Location` varchar(255) DEFAULT NULL,
  `Status` enum('Active','Archived') NOT NULL DEFAULT 'Active',
  `CreatedAt` timestamp NULL DEFAULT current_timestamp(),
  `UpdatedAt` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`JobAdID`),
  KEY `fk_CompanyID_idx` (`CompanyID`),
  KEY `idx_status_on_jobad` (`Status`),
  KEY `idx_location_on_jobad` (`Location`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jobadinteraction`
--

DROP TABLE IF EXISTS `jobadinteraction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobadinteraction` (
  `InteractionID` int(11) NOT NULL AUTO_INCREMENT,
  `ProfessionalID` int(11) DEFAULT NULL,
  `JobAdID` int(11) DEFAULT NULL,
  `InteractionType` varchar(255) DEFAULT NULL,
  `InteractionTimestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`InteractionID`),
  KEY `fk_ProfessionalID_idx` (`ProfessionalID`),
  KEY `fk_JobAdID_idx` (`JobAdID`),
  CONSTRAINT `jobadinteraction_ibfk_1` FOREIGN KEY (`ProfessionalID`) REFERENCES `professional` (`ProfessionalID`),
  CONSTRAINT `jobadinteraction_ibfk_2` FOREIGN KEY (`JobAdID`) REFERENCES `jobad` (`JobAdID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jobadskill`
--

DROP TABLE IF EXISTS `jobadskill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobadskill` (
  `JobAdID` int(11) NOT NULL,
  `SkillID` int(11) NOT NULL,
  `Level` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`JobAdID`,`SkillID`),
  KEY `fk_JobAdID_idx` (`JobAdID`),
  KEY `fk_SkillID_idx` (`SkillID`),
  CONSTRAINT `jobadskill_ibfk_1` FOREIGN KEY (`JobAdID`) REFERENCES `jobad` (`JobAdID`),
  CONSTRAINT `jobadskill_ibfk_2` FOREIGN KEY (`SkillID`) REFERENCES `skill` (`SkillID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `matchrequests`
--

DROP TABLE IF EXISTS `matchrequests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `matchrequests` (
  `RequestID` int(11) NOT NULL AUTO_INCREMENT,
  `ProfessionalID` int(11) DEFAULT NULL,
  `CompanyAdID` int(11) DEFAULT NULL,
  `CompanyID` int(11) DEFAULT NULL,
  `JobAdID` int(11) DEFAULT NULL,
  `MatchStatus` enum('Pending','Accepted','Rejected') NOT NULL DEFAULT 'Pending',
  `ProcessedAt` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `SentAt` timestamp NOT NULL DEFAULT current_timestamp(),
  `InitializedBy` enum('Professional','Company') NOT NULL,
  PRIMARY KEY (`RequestID`),
  KEY `fk_CompanyAdID_idx` (`CompanyAdID`),
  KEY `fk_JobAdID_idx` (`JobAdID`),
  KEY `idx_matchstatus_on_matchrequests` (`MatchStatus`),
  KEY `fk_matchrequests_companyID` (`CompanyID`),
  KEY `fk_matchrequests_professionalID` (`ProfessionalID`),
  CONSTRAINT `fk_match_requests_companyad` FOREIGN KEY (`CompanyAdID`) REFERENCES `companyad` (`CompanyAdID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_matchrequests_companyID` FOREIGN KEY (`CompanyID`) REFERENCES `company` (`CompanyID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_matchrequests_jobad1` FOREIGN KEY (`JobAdID`) REFERENCES `jobad` (`JobAdID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_matchrequests_professionalID` FOREIGN KEY (`ProfessionalID`) REFERENCES `professional` (`ProfessionalID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS `notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notification` (
  `NotificationID` int(11) NOT NULL AUTO_INCREMENT,
  `RecipientID` int(11) DEFAULT NULL,
  `RecipientType` enum('Professional','Company') DEFAULT NULL,
  `RequestID` int(11) DEFAULT NULL,
  `Message` text DEFAULT NULL,
  `IsRead` tinyint(1) DEFAULT 0,
  `CreatedAt` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`NotificationID`),
  KEY `fk_RequestID_idx` (`RequestID`),
  KEY `idx_recipient_on_notification` (`RecipientID`,`RecipientType`),
  KEY `idx_isread_on_notification` (`IsRead`),
  CONSTRAINT `notification_ibfk_1` FOREIGN KEY (`RequestID`) REFERENCES `matchrequests` (`RequestID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `professional`
--

DROP TABLE IF EXISTS `professional`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `professional` (
  `ProfessionalID` int(11) NOT NULL AUTO_INCREMENT,
  `Username` varchar(255) DEFAULT NULL,
  `FirstName` varchar(255) DEFAULT NULL,
  `LastName` varchar(255) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `BriefSummary` text DEFAULT NULL,
  `Location` varchar(255) DEFAULT NULL,
  `Status` enum('Active','Busy') NOT NULL DEFAULT 'Active',
  `PhotoURL` varchar(255) DEFAULT NULL,
  `CVURL` varchar(255) DEFAULT NULL,
  `Contact` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `ProfessionalEmail` varchar(255) NOT NULL,
  `VerificationToken` varchar(255) DEFAULT NULL,
  `EmailVerified` tinyint(1) DEFAULT 0,
  `MainAd` int(11) DEFAULT NULL,
  `is_blocked` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`ProfessionalID`),
  UNIQUE KEY `ProfessionalEmail_UNIQUE` (`ProfessionalEmail`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `skill`
--

DROP TABLE IF EXISTS `skill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skill` (
  `SkillID` int(11) NOT NULL AUTO_INCREMENT,
  `Description` text DEFAULT NULL,
  PRIMARY KEY (`SkillID`),
  UNIQUE KEY `Description_UNIQUE` (`Description`(255))
) ENGINE=InnoDB AUTO_INCREMENT=174 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-07 12:13:27
