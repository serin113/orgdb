-- Created in 2019-01-31 for PSYSC as part of a system for managing science club affiliations.

-- Copyright (c) 2019 Nathankissam Roy Tubis & Elfren Simon Clemente.
-- Licensed under the MIT License, refer to https://opensource.org/licenses/MIT for details.

-- Code History:
-- 2019/02/06 (Nathan) - Initial working code and documentation
-- 2019/02/17 (Simon) - Cleanup to follow same format as the mysqldump output
-- 2019/02/27 (Nathan) - Added table for affiliation application
-- 2019/02/27 (Simon) - Cleanup & additional documentation
-- 2019/03/02 (Simon) - Added command to drop database every time this file is sourced
-- 2019/03/07 (Simon) - Fixed data types
-- 2019/03/26 (Simon) - Added LoginCredentialsTable and LoginAccessTable
--                    - Changed appID and affiliationID lengths to 128 (for SHA-512 hex hash)
-- 2019/04/05 (Simon) - Updated some fields to to be required ("NOT NULL")

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';


DROP DATABASE IF EXISTS `mydb`;
CREATE DATABASE `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;


-- -----------------------------------------------------
-- Table `AffiliationRecordsTable`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AffiliationRecordsTable`;
CREATE TABLE IF NOT EXISTS `AffiliationRecordsTable` (
  `clubID` VARCHAR(50) NOT NULL,    -- record-unique id
  `dateUpdated` DATETIME NOT NULL,      -- record last modification date
  `region` TINYINT(1) NULL,         -- school's regional PSGC: 1 to 17
                                    -- https://psa.gov.ph/classification/psgc/downloads/SUMWEBPROV-DEC2018-CODED-HUC-FINAL.pdf
  `level` TINYINT(1) NULL,          -- 1: elementary
                                    -- 2: high school
                                    -- 3: elementary + high school
                                    -- 4: college
  `type` TINYINT(1) NULL,           -- 1: public, 2: private, 3: SCU (state college/uni)
  `school` VARCHAR(100) NULL,       -- name of school
  `clubName` VARCHAR(100) NULL,     -- name of club
  `address` VARCHAR(200) NULL,      -- school's address
  `city` VARCHAR(100) NULL,          -- school's city
  `province` VARCHAR(100) NULL,      -- school's province
  `adviserName` VARCHAR(100) NULL,  -- club adviser/s' name
  `contact` VARCHAR(100) NULL,       -- club contact no.
  `email` VARCHAR(100) NULL,         -- club email
  PRIMARY KEY (`clubID`))
ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- -----------------------------------------------------
-- Table `mydb`.`AffiliationTable`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AffiliationTable`;
CREATE TABLE IF NOT EXISTS `AffiliationTable` (
  `affiliationID` VARCHAR(128) NOT NULL,     -- affiliation-unique id
  `affiliated` TINYINT(1) NOT NULL,         -- is club affiliated? 0:no, 1:yes
  `status` VARCHAR(45) NULL,                -- "newly affiliated", "renewing", etc.
  `hasAffiliationForms` TINYINT(1) NULL,    -- are forms submitted? 0:no, 1:yes
  `benefits` VARCHAR(200) NULL,             -- any discounts/sponsorships/scholarships/etc.
  `remarks` VARCHAR(200) NULL,              -- extra remarks
  `schoolYear` YEAR(4) NOT NULL,                -- if s.y. 2018-2019, store 2019
  `yearsAffiliated` INT(11) NOT NULL,               -- duration of affiliation
  `SCA` SMALLINT(10) NOT NULL,                  -- # of club advisers
  `SCM` SMALLINT(10) NOT NULL,                  -- # of club members
  `paymentMode` VARCHAR(200) NULL,          -- means of payment (deposit/check/etc.)
  `paymentDate` DATETIME NULL,                  -- date paid
  `paymentID` VARCHAR(200) NULL,            -- identifier for payment
  `paymentAmount` INT(11) NULL,                 -- amount paid
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


-- -----------------------------------------------------
-- Table `AffiliationApplicationsTable`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AffiliationApplicationsTable`;
CREATE TABLE `AffiliationApplicationsTable` (
  `appID` VARCHAR(128) NOT NULL,     -- application-unique ID
  `hasRecord` TINYINT(4) NULL,      -- is this application for an existing record? 0:no, 1:yes
  `clubID` VARCHAR(50) NULL,        -- (only used if hasRecord is 1) for which club?
  `dateCreated` DATETIME NOT NULL,  -- date application is created
  /* same fields as in AffiliationTable & AffiliationRecordsTable */
  `region` TINYINT(1) NULL,         -- (only used if hasRecord is 0)
  `level` TINYINT(1) NULL,          -- (only used if hasRecord is 0)
  `type` TINYINT(1) NULL,           -- (only used if hasRecord is 0)
  `school` VARCHAR(200) NULL,       -- (only used if hasRecord is 0)
  `clubName` VARCHAR(200) NULL,     -- (only used if hasRecord is 0)
  `address` VARCHAR(500) NULL,      -- (only used if hasRecord is 0)
  `city` VARCHAR(100) NULL,         -- (only used if hasRecord is 0)
  `province` VARCHAR(100) NULL,     -- (only used if hasRecord is 0)
  `adviserName` VARCHAR(100) NULL,  -- (only used if hasRecord is 0)
  `contact` VARCHAR(100) NULL,      -- (only used if hasRecord is 0)
  `email` VARCHAR(100) NULL,        -- (only used if hasRecord is 0)
  `schoolYear` YEAR(4) NULL,
  `yearsAffiliated` INT(11) NULL,
  `SCA` SMALLINT(10) NULL,
  `SCM` SMALLINT(10) NULL,
  `paymentMode` VARCHAR(100) NULL,
  `paymentDate` DATE NULL,
  `paymentID` VARCHAR(200) NULL,
  `paymentAmount` INT(11) NULL,
  `receiptNumber` VARCHAR(200) NULL,
  `paymentSendMode` VARCHAR(200) NULL,
  PRIMARY KEY (`appID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- -----------------------------------------------------
-- Table `LoginCredentialsTable`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `LoginCredentialsTable`;
CREATE TABLE `LoginCredentialsTable` (
  `ID` VARCHAR(50) NOT NULL,        -- login ID
  `PINHash` VARCHAR(128) NOT NULL,  -- (assumes 512-bit hash in hex) (hashed as <password><salt>)
  `PINSalt` VARCHAR(64) NOT NULL,   -- (assumes 256-bit salt in hex)
  `Type` TINYINT(1) NOT NULL,       -- 0 if Club, 1 if Admin
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- -----------------------------------------------------
-- Table `LoginAccessTable`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `LoginAccessTable`;
CREATE TABLE `LoginAccessTable` (
  `ID` VARCHAR(50) NOT NULL,        -- login ID
  `Token` VARCHAR(128) NOT NULL,    -- (assumes 512-bit access token in hex)
  `Expires` DATETIME NOT NULL       -- datetime of expiry of token (YYYY-MM-DD HH:MM:SS)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
