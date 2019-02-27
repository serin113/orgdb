-- Created in 2019-01-31 for PSYSC as part of a system for managing science club affiliations.

-- Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
-- Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

-- Code History:
-- 2019/02/06 (Nathan) - Initial working code and documentation
-- 2019/02/17 (Simon) - Cleanup to follow same format as the mysqldump output
-- 2019/02/27 (Nathan) - Added table for affiliation application

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';


CREATE DATABASE IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `AffiliationRecordsTable`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `affiliationapplication`;
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

-- -----------------------------------------------------
-- Table `AffiliationRecordsTable`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AffiliationRecordsTable` ;

CREATE TABLE IF NOT EXISTS `AffiliationRecordsTable` (
  `clubID` VARCHAR(50) NOT NULL,    -- record-unique id
  `dateUpdated` DATE NOT NULL,      -- record last modification date
  `region` VARCHAR(10) NULL,        -- school's regional PSGC: 1 to 17
                                    -- https://psa.gov.ph/classification/psgc/downloads/SUMWEBPROV-DEC2018-CODED-HUC-FINAL.pdf
  `level` TINYINT(1) NULL,          -- 1: elementary
                                    -- 2: high school
                                    -- 3: elementary + high school
                                    -- 4: college
  `type` TINYINT(1) NULL,           -- 1: public, 2: private
  `school` VARCHAR(100) NULL,       -- name of school
  `clubName` VARCHAR(100) NULL,     -- name of club
  `address` VARCHAR(200) NULL,      -- school's address
  `city` VARCHAR(45) NULL,          -- school's city
  `province` VARCHAR(45) NULL,      -- school's province
  `adviserName` VARCHAR(100) NULL,  -- club adviser/s' name
  `contact` VARCHAR(45) NULL,       -- club contact no.
  `email` VARCHAR(45) NULL,         -- club email
  PRIMARY KEY (`clubID`))
ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- -----------------------------------------------------
-- Table `mydb`.`AffiliationTable`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AffiliationTable` ;

CREATE TABLE IF NOT EXISTS `AffiliationTable` (
  `affiliationID` VARCHAR(50) NOT NULL,    -- affiliation-unique id
  `affiliated` TINYINT(1) NOT NULL,         -- is club affiliated? 0:no, 1:yes
  `status` VARCHAR(45) NULL,                -- "newly affiliated", "renewing", etc.
  `hasAffiliationForms` TINYINT(1) NULL,    -- are forms submitted? 0:no, 1:yes
  `benefits` VARCHAR(200) NULL,             -- any discounts/sponsorships/scholarships/etc.
  `remarks` VARCHAR(200) NULL,              -- extra remarks
  `schoolYear` YEAR(4) NULL,                -- if s.y. 2018-2019, store 2019
  `yearsAffiliated` INT NULL,               -- duration of affiliation
  `SCA` SMALLINT(10) NULL,                  -- # of club advisers
  `SCM` SMALLINT(10) NULL,                  -- # of club members
  `paymentMode` VARCHAR(200) NULL,          -- means of payment (deposit/check/etc.)
  `paymentDate` DATE NULL,                  -- date paid
  `paymentID` VARCHAR(200) NULL,            -- identifier for payment
  `paymentAmount` INT NULL,                 -- amount paid
  `receiptNumber` VARCHAR(200) NULL,        -- payment receipt number
  `paymentSendMode` VARCHAR(200) NULL,      -- means of sending payment (delivery/in-person/etc.)
  `AffiliationRecordsTable_clubID` VARCHAR(50) NOT NULL,    -- affiliation under which club?
  PRIMARY KEY (`affiliationID`, `AffiliationRecordsTable_clubID`),
  KEY `fk_AffiliationTable_AffiliationRecordsTable_idx` (`AffiliationRecordsTable_clubID`),
  CONSTRAINT `fk_AffiliationTable_AffiliationRecordsTable`
    FOREIGN KEY (`AffiliationRecordsTable_clubID`)
    REFERENCES `AffiliationRecordsTable` (`clubID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE=InnoDB DEFAULT CHARSET=utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
