--  创建db
CREATE DATABASE IF NOT EXISTS share DEFAULT CHARSET utf8 COLLATE utf8_general_ci;


-- 股票
CREATE TABLE IF NOT EXISTS `shares`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `code` VARCHAR(40) NOT NULL,
   `name` VARCHAR(40) NOT NULL,
   `update_date` TIMESTAMP,
   `create_date` TIMESTAMP,
   PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 基金
CREATE TABLE IF NOT EXISTS `funds`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `code` VARCHAR(40) NOT NULL, -- 代码
   `name` VARCHAR(40) NOT NULL, -- 基金名称
   `positions` VARCHAR(21812) NOT NULL, -- 持仓占比
   `update_date` TIMESTAMP,
   `create_date` TIMESTAMP,
   PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 交易
-- date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,pbMRQ,peTTM,psTTM,pcfNcfTTM,isST
CREATE TABLE IF NOT EXISTS `shares`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `code` VARCHAR(40) NOT NULL,
   `open` float(20,2) DEFAULT NULL,
   `high` float(20,2) DEFAULT NULL,
   `low` float(20,2) DEFAULT NULL,
   `close` float(20,2) DEFAULT NULL,
   `preclose` float(20,2) DEFAULT NULL,
   `volume` float(20,2) DEFAULT NULL,
   `amount` float(20,2) DEFAULT NULL,
   `adjustflag` int(1) default NULL,
   `turn` float(20,2) DEFAULT NULL,
   `tradestatus` int(1) default NULL,
   `pctChg` float(20,2) DEFAULT NULL,
   `pbMRQ` float(20,2) DEFAULT NULL,
   `peTTM` float(20,2) DEFAULT NULL,
   `psTTM` float(20,2) DEFAULT NULL,
   `pcfNcfTTM` float(20,2) DEFAULT NULL,
   `isST` int(1) DEFAULT NULL,

   `share_fund` varchar(10) DEFAULT NULL,  -- 类型 股票/基金
   `date` TIMESTAMP,
   `update_date` TIMESTAMP,
   `create_date` TIMESTAMP,
   PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

