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
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (2,'admin','$2b$12$.2Dkq/re5Q9WpkVM.Js.8OX/DqMiBBKnIw3sTi.JEqzqO.Q0j9YOa');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auditlog`
--

LOCK TABLES `auditlog` WRITE;
/*!40000 ALTER TABLE `auditlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `auditlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `company`
--

LOCK TABLES `company` WRITE;
/*!40000 ALTER TABLE `company` DISABLE KEYS */;
INSERT INTO `company` VALUES (35,'mario','MarioSt','$2b$12$XyusZpk7h4u.0zIFcT7cIe9JarPQYAyOYqP8I2i7oq8JCjzBEwqgq',NULL,NULL,NULL,NULL,'mario@gmail.com','5ad9d4b6-0bf7-451a-81da-c44222bd819a',0,0),(36,'stephcurry','StephenCurry','$2b$12$Wt5nLjo2EkwxkNT4KxSG0Ohrg6ZRp.yqBmIWT5AHKTJx43lSzD8um',NULL,NULL,NULL,NULL,'stephcurry@gmail.com','0fcf93ac-18b7-4bc2-8041-2483f86838b8',0,0),(37,'kd','KevinDurant','$2b$12$mhMpdLuN3S.Rk0C3U9lUXuUjqr6uHL54d23VLMNVuY4Ifs/i6SP/i',NULL,NULL,NULL,NULL,'kd@gmail.com','09d6f1d7-34e4-404f-b97b-927f7d72de0c',0,0),(38,'mario2','MarioOOD','$2b$12$9hDFRZe96bohH2o72PsWQuGGGKxHzkQ67uLNRaBLEqXSS9dOSbgaC',NULL,NULL,NULL,NULL,'mariost2@gmail.com','1ba36a31-5b68-462d-ad7e-a94acdf6fb4b',0,0),(40,'buildpro12','BuildPro','$2b$12$/3beWXG8W.5KvAPNLKmTs.ntgQW3C9.V8pHg7bwCtqk6jbIbV9Zfa','Building company','New York City','exampleimage','www.buildpro12.com','bpro@mail.com','404d655c-9ab7-4c08-926b-ec9b1b86f12b',1,0),(42,'alphateam8','AlphaTeamIT','$2b$12$249PdmdvTmN1BSsOEeqRT.bMYbZWYMaQuPWhpHxPizhTuqO9.b2AS','IT Company','Plovdiv','examplepic','0871231231','alphateam8@gmail.com','fe382b10-b761-4893-ac59-14e811dcd406',0,0),(43,'itcompany','ITCompany','$2b$12$leSsr48qSpFkVHZ.3q9M7OBXFuvQaAIIIlTS1s3OmIa1WaZoTFkxO',NULL,NULL,NULL,NULL,'itcompany@gmail.com','4f3619b8-2cd7-42c2-a1fa-981eb3900841',0,0),(44,'companyit','CompanyIT','$2b$12$xlewlWLsyf1xaniZP.85R.oOcPzi5E/iMhi7/D1Bi6LSAWxz1GNEe','IT Company','Sofia','examplepicture','0871231231','companyit@gmail.com','a51031aa-c544-47a7-9737-f16cb194acb4',0,0);
/*!40000 ALTER TABLE `company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `companyad`
--

LOCK TABLES `companyad` WRITE;
/*!40000 ALTER TABLE `companyad` DISABLE KEYS */;
INSERT INTO `companyad` VALUES (29,16,37000000,42000000,'I am a great shooting guard!','San Francisco','Active','I prefer the Golden State Warriors as a team.','2023-12-07 11:18:56','2023-12-07 15:12:20'),(30,18,30000000,40000000,'Very good defender!','San Francisco','Active','I prefer the Golden State Warriors as a team.','2023-12-07 12:17:21','2023-12-07 12:17:21'),(31,18,10000,20000,'Builder','Sofia','Active','More money.','2023-12-07 12:19:53','2023-12-07 12:19:53'),(34,16,15000000,20000000,'Expert catch-n-shoot guard!','San Francisco','Active','I also wouldn\'t mind Miami Heat.','2023-12-07 12:39:44','2023-12-07 12:39:44'),(35,16,35000000,45000000,'Great dribbler!','San Francisco','Active','Would want to play for the Denver Nuggets! cap.','2023-12-07 12:41:20','2023-12-07 12:42:05'),(36,16,1000,1200,'KFC','Sofia','Active','KFC is not bad too.','2023-12-07 12:50:38','2023-12-07 12:50:38'),(37,16,980,1220,'McDonalds guy','Sofia','Active','McDonalds is the best.','2023-12-07 12:51:46','2023-12-07 12:51:46'),(38,19,49000,60000,'Experienced Project Manager','New York','Archived','Health benefits','2023-12-07 13:58:59','2023-12-07 14:03:58');
/*!40000 ALTER TABLE `companyad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `companyadskill`
--

LOCK TABLES `companyadskill` WRITE;
/*!40000 ALTER TABLE `companyadskill` DISABLE KEYS */;
INSERT INTO `companyadskill` VALUES (29,182,'Unstoppable'),(30,182,'Expert'),(31,189,'Pro'),(31,190,'Medium'),(34,182,'Expert'),(34,199,'Expert'),(34,200,'Expert'),(35,182,'Expert'),(35,199,'Expert'),(35,200,'Expert'),(36,210,'Expert'),(37,211,'Expert'),(38,185,'3years');
/*!40000 ALTER TABLE `companyadskill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `jobad`
--

LOCK TABLES `jobad` WRITE;
/*!40000 ALTER TABLE `jobad` DISABLE KEYS */;
INSERT INTO `jobad` VALUES (59,35,1900,2500,'Python Intern','Sofia','Active','2023-12-07 11:04:47','2023-12-07 11:05:25'),(61,36,100000,150000,'Master Chef','San Francisco','Active','2023-12-07 11:08:08','2023-12-07 11:08:08'),(63,37,20000,25000,'Chauffeur','Phoenix, Arizona','Active','2023-12-07 11:12:56','2023-12-07 11:12:56'),(64,37,10000,30000,'Bodyguard','Phoenix, Arizona','Active','2023-12-07 11:14:58','2023-12-07 11:14:58'),(65,40,55000,75000,'We are seeking an experienced Construction Project Manager to join our dynamic team. The ideal candidate will have a strong background in civil engineering or a related field, with proven experience in managing large-scale construction projects. Responsibilities include overseeing project progress, managing budgets, ensuring safety regulations, and coordinating with various teams.','New York City','Active','2023-12-07 12:13:38','2023-12-07 12:15:08'),(66,42,8500,10500,'Senior Java Developer','Plovdiv','Active','2023-12-07 12:33:53','2023-12-07 12:34:40'),(67,43,1700,2200,'Python Intern','Sofia','Active','2023-12-07 15:02:42','2023-12-07 15:03:13');
/*!40000 ALTER TABLE `jobad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `jobadinteraction`
--

LOCK TABLES `jobadinteraction` WRITE;
/*!40000 ALTER TABLE `jobadinteraction` DISABLE KEYS */;
/*!40000 ALTER TABLE `jobadinteraction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `jobadskill`
--

LOCK TABLES `jobadskill` WRITE;
/*!40000 ALTER TABLE `jobadskill` DISABLE KEYS */;
INSERT INTO `jobadskill` VALUES (59,174,'Good'),(61,177,'Expert'),(63,180,'Expert'),(64,181,'Expert'),(65,184,'3years'),(65,185,'2years.'),(66,192,'Expert'),(66,193,'Pro'),(66,194,'Pro'),(67,174,'Beginner'),(67,213,'Beginner'),(67,217,'Beginner');
/*!40000 ALTER TABLE `jobadskill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `matchrequests`
--

LOCK TABLES `matchrequests` WRITE;
/*!40000 ALTER TABLE `matchrequests` DISABLE KEYS */;
INSERT INTO `matchrequests` VALUES (26,19,NULL,NULL,65,'Pending','2023-12-07 14:26:47','2023-12-07 14:26:47','Professional'),(27,19,NULL,40,NULL,'Pending','2023-12-07 14:26:53','2023-12-07 14:26:53','Professional'),(28,NULL,38,40,NULL,'Accepted','2023-12-07 14:27:46','2023-12-07 14:27:08','Company'),(29,19,NULL,40,NULL,'Pending','2023-12-07 14:27:14','2023-12-07 14:27:14','Company');
/*!40000 ALTER TABLE `matchrequests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `notification`
--

LOCK TABLES `notification` WRITE;
/*!40000 ALTER TABLE `notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `professional`
--

LOCK TABLES `professional` WRITE;
/*!40000 ALTER TABLE `professional` DISABLE KEYS */;
INSERT INTO `professional` VALUES (16,'klay','Klay','Thompson','$2b$12$nocMM/vdTPGMVpLSJ.Y1FOMpNYB89orGf/PxIWHWRPkhNqTdUcNCm','An expert shooting guard.','San Francisco','Active','examplephoto','somecvurl','087987987',NULL,'klay@gmail.com','9f1d17cd-4a42-45b4-87d7-ef950e6dec6f',0,29,0),(17,'ben','Ben','Simmons','$2b$12$XPWtqnFGEJDYg20AZPNjFOuqUUnLs2nEz2C7pF1IMzMzLJKWPqlVi',NULL,NULL,'Active',NULL,NULL,NULL,NULL,'ben@gmail.com','36af0e49-1945-4547-9e11-9fed15686c7f',0,NULL,0),(18,'dray','Draymond','Green','$2b$12$xY3BWhduOWnq07o6MGnSq.SlJsNnmVKsQScXJXTAEWaZb0oomIIky',NULL,NULL,'Active',NULL,NULL,NULL,NULL,'dray@gmail.com','ccfd1da5-71ff-4033-83f0-0b0dd4639cb6',0,NULL,0),(19,'Dean89','Dean','Smith','$2b$12$QvKVRFhGP.QRTzxalTWZ2uHodUgtiS7pt1oAbpWDzrbaLL/0qNUDK',NULL,NULL,'Busy',NULL,NULL,NULL,NULL,'dean89@test.com',NULL,0,NULL,1);
/*!40000 ALTER TABLE `professional` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `skill`
--

LOCK TABLES `skill` WRITE;
/*!40000 ALTER TABLE `skill` DISABLE KEYS */;
INSERT INTO `skill` VALUES (174,'Developer'),(177,'Cooking'),(178,'Physiotherapist'),(179,'Chauffeur'),(180,'Driving'),(181,'Bodyguarding'),(182,'Basketball'),(184,'Project Management'),(185,'Budgeting'),(189,'Plastering'),(190,'Painting'),(191,'Cleaning'),(192,'Java'),(193,'AWS'),(194,'SQL'),(199,'Shooting'),(200,'Defence'),(210,'KFC'),(211,'McDonalds'),(213,'Python'),(217,'HTML');
/*!40000 ALTER TABLE `skill` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-07 18:53:12
