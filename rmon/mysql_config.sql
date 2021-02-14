CREATE DATABASE rmon; 
USE rmon; 


-- TABLA ts_filter

CREATE TABLE ts_filter ( oid TEXT, orden INT, name TEXT, next_table TEXT, type_value TEXT, value TEXT, access INT, staus TEXT, next_oid TEXT );

INSERT INTO ts_filter VALUES ( '1.3.6.1.2.1.16.7.1', '1', 'filterTable', 'tc_filterEntry', 'SEQUENCE OF FilterEntry', 'NONE', '0', 'mandatory', '1.3.6.1.2.1.16.7.1.1.1' );

INSERT INTO ts_filter VALUES ( '1.3.6.1.2.1.16.7.2', '2', 'channelTable', 'tc_channelEntry', 'SEQUENCE OF ChannelEntry', 'NONE', '0', 'mandatory', '1.3.6.1.2.1.16.7.2.1.1' );


-- TABLA tc_filterEntry

CREATE TABLE tc_filterEntry ( oid TEXT, orden INT, name TEXT, next_table TEXT, indices TEXT, type_value TEXT, value TEXT, access INT, staus TEXT, next_oid TEXT );

INSERT INTO tc_filterEntry VALUES ( '1.3.6.1.2.1.16.7.1.1.1', '1', 'filterIndex', 'td_filterEntry', 'filterIndex', 'INTEGER', '0', '1', 'mandatory', '1.3.6.1.2.1.16.7.1.1.2' );

INSERT INTO tc_filterEntry VALUES ( '1.3.6.1.2.1.16.7.1.1.2', '2', 'filterChannelIndex', 'td_filterEntry', 'filterIndex', 'INTEGER', '0', '3', 'mandatory', '1.3.6.1.2.1.16.7.1.1.3' );

INSERT INTO tc_filterEntry VALUES ( '1.3.6.1.2.1.16.7.1.1.3', '3', 'filterPktDataOffset', 'td_filterEntry', 'filterIndex', 'INTEGER', '0', '3', 'mandatory', '1.3.6.1.2.1.16.7.1.1.4' );

INSERT INTO tc_filterEntry VALUES ( '1.3.6.1.2.1.16.7.1.1.4', '4', 'filterPktData', 'td_filterEntry', 'filterIndex', 'OctetString', '0', '3', 'mandatory', '1.3.6.1.2.1.16.7.1.1.5' );

INSERT INTO tc_filterEntry VALUES ( '1.3.6.1.2.1.16.7.1.1.5', '5', 'filterPktDataMask', 'td_filterEntry', 'filterIndex', 'OctetString', '0', '3', 'mandatory', '1.3.6.1.2.1.16.7.1.1.6' );

INSERT INTO tc_filterEntry VALUES ( '1.3.6.1.2.1.16.7.1.1.6', '6', 'filterPktDataNotMask', 'td_filterEntry', 'filterIndex', 'OctetString', '0', '3', 'mandatory', '1.3.6.1.2.1.16.7.1.1.7' );

INSERT INTO tc_filterEntry VALUES ( '1.3.6.1.2.1.16.7.1.1.7', '7', 'filterPktStatus', 'td_filterEntry', 'filterIndex', 'INTEGER', '0', '3', 'mandatory', '1.3.6.1.2.1.16.7.1.1.8' );

INSERT INTO tc_filterEntry VALUES ( '1.3.6.1.2.1.16.7.1.1.8', '8', 'filterPktStatusMask', 'td_filterEntry', 'filterIndex', 'INTEGER', '0', '3', 'mandatory', '1.3.6.1.2.1.16.7.1.1.9' );

INSERT INTO tc_filterEntry VALUES ( '1.3.6.1.2.1.16.7.1.1.9', '9', 'filterPktStatusNotMask', 'td_filterEntry', 'filterIndex', 'INTEGER', '0', '3', 'mandatory', '1.3.6.1.2.1.16.7.1.1.10' );

INSERT INTO tc_filterEntry VALUES ( '1.3.6.1.2.1.16.7.1.1.10', '10', 'filterOwner', 'td_filterEntry', 'filterIndex', 'OctetString', '0', '3', 'mandatory', '1.3.6.1.2.1.16.7.1.1.11' );

INSERT INTO tc_filterEntry VALUES ( '1.3.6.1.2.1.16.7.1.1.11', '11', 'filterStatus', 'td_filterEntry', 'filterIndex', 'INTEGER', '0', '3', 'mandatory', '1.3.6.1.2.1.16.7.2.1.1' );


-- Tabla tc_channelEntry

CREATE TABLE tc_channelEntry ( oid TEXT, orden INT(8), name TEXT, next_table TEXT, indices TEXT, type_value TEXT, value TEXT, access INT(2), staus TEXT, next_oid TEXT );

INSERT INTO tc_channelEntry VALUES ( '1.3.6.1.2.1.16.7.2.1.1', '1', 'channelIndex', 'td_channelEntry', 'channelIndex', 'INTEGER', '0', '1', 'mandatory', '1.3.6.1.2.1.16.7.2.1.2' );

INSERT INTO tc_channelEntry VALUES ( '1.3.6.1.2.1.16.7.2.1.2', '2', 'channelIfIndex', 'td_channelEntry', 'channelIndex', 'INTEGER', '0', '3', 'mandatory', '1.3.6.1.2.1.16.7.2.1.3' );

INSERT INTO tc_channelEntry VALUES ( '1.3.6.1.2.1.16.7.2.1.3', '3', 'channelAcceptType', 'td_channelEntry', 'channelIndex', 'INTEGER', '0', '3', 'mandatory', '1.3.6.1.2.1.16.7.2.1.4' );

INSERT INTO tc_channelEntry VALUES ( '1.3.6.1.2.1.16.7.2.1.4', '4', 'channelDataControl', 'td_channelEntry', 'channelIndex', 'INTEGER', '0', '3', 'mandatory', '1.3.6.1.2.1.16.7.2.1.5' );

INSERT INTO tc_channelEntry VALUES ( '1.3.6.1.2.1.16.7.2.1.5', '5', 'channelTurnOnEventIndex', 'td_channelEntry', 'channelIndex', 'INTEGER', '0', '3', 'mandatory', '1.3.6.1.2.1.16.7.2.1.6' );

INSERT INTO tc_channelEntry VALUES ( '1.3.6.1.2.1.16.7.2.1.6', '6', 'channelTurnOffEventIndex', 'td_channelEntry', 'channelIndex', 'INTEGER', '0', '3', 'mandatory', '1.3.6.1.2.1.16.7.2.1.7' );

INSERT INTO tc_channelEntry VALUES ( '1.3.6.1.2.1.16.7.2.1.7', '7', 'channelEventIndex', 'td_channelEntry', 'channelIndex', 'INTEGER', '0', '3', 'mandatory', '1.3.6.1.2.1.16.7.2.1.8' );

INSERT INTO tc_channelEntry VALUES ( '1.3.6.1.2.1.16.7.2.1.8', '8', 'channelEventStatus', 'td_channelEntry', 'channelIndex', 'INTEGER', '0', '3', 'mandatory', '1.3.6.1.2.1.16.7.2.1.9' );

INSERT INTO tc_channelEntry VALUES ( '1.3.6.1.2.1.16.7.2.1.9', '9', 'channelMatches', 'td_channelEntry', 'channelIndex', 'Counter', '0', '1', 'mandatory', '1.3.6.1.2.1.16.7.2.1.10' );

INSERT INTO tc_channelEntry VALUES ( '1.3.6.1.2.1.16.7.2.1.10', '10', 'channelDescription', 'td_channelEntry', 'channelIndex', 'OctetString', '0', '3', 'mandatory', '1.3.6.1.2.1.16.7.2.1.11' );

INSERT INTO tc_channelEntry VALUES ( '1.3.6.1.2.1.16.7.2.1.11', '11', 'channelOwner', 'td_channelEntry', 'channelIndex', 'OctetString', '0', '3', 'mandatory', '1.3.6.1.2.1.16.7.2.1.12' );

INSERT INTO tc_channelEntry VALUES ( '1.3.6.1.2.1.16.7.2.1.12', '12', 'channelStatus', 'td_channelEntry', 'channelIndex', 'INTEGER', '0', '3', 'mandatory', '1.3.6.1.2.1.16.8.1.1.1' );


-- TABLA td_filterEntry

CREATE TABLE td_filterEntry ( filterIndex INT(8) PRIMARY KEY, filterChannelIndex INT(8) DEFAULT 0, filterPktDataOffset INT(8) DEFAULT 0, filterPktData VARCHAR(255) DEFAULT ' ', filterPktDataMask VARCHAR(255) DEFAULT ' ', filterPktDataNotMask VARCHAR(255) DEFAULT ' ', filterPktStatus INT(3) DEFAULT 0, filterPktStatusMask INT(3) DEFAULT 0, filterPktStatusNotMask INT(3) DEFAULT 0, filterOwner VARCHAR(255) DEFAULT ' ', filterStatus INT(3) );


-- TABLA td_channelEntry

CREATE TABLE td_channelEntry ( channelIndex INT(8) PRIMARY KEY, channelIfIndex INT(8) DEFAULT 0, channelAcceptType INT(2) DEFAULT 0, channelDataControl INT(2) DEFAULT 0, channelTurnOnEventIndex INT(8) DEFAULT 0, channelTurnOffEventIndex INT(8) DEFAULT 0, channelEventIndex INT(8) DEFAULT 0, channelEventStatus INT(2) DEFAULT 0, channelMatches INT(8) DEFAULT 0, channelDescription VARCHAR(255) DEFAULT ' ', channelOwner VARCHAR(255) DEFAULT ' ', channelStatus INT(3) );







CREATE DATABASE comunidades; 
USE comunidades; 



-- Tabla ts_comunidades

CREATE TABLE ts_comunidades ( oid TEXT, orden INT, name TEXT, next_table TEXT, type_value TEXT, value TEXT, access INT, staus TEXT, next_oid TEXT );

INSERT INTO ts_comunidades VALUES ( '1.3.6.1.4.1.28308.1', '1', 'master', 'nextTable', 'OctetString', 'admin', '3', 'mandatory', '1.3.6.1.4.1.28308.2.1.1' );

INSERT INTO ts_comunidades VALUES ( '1.3.6.1.4.1.28308.2', '2', 'communityTable', 'tc_communityManagement', 'SEQUENCE OF CommunityEntry', 'NONE', '0', 'mandatory', '1.3.6.1.4.1.28309' );


-- Tabla tc_comunidades

CREATE TABLE tc_communityManagement ( oid TEXT, orden INT(8), name TEXT, next_table TEXT, indices TEXT, type_value TEXT, value TEXT, access INT(2), staus TEXT, next_oid TEXT );

INSERT INTO tc_communityManagement VALUES ( '1.3.6.1.4.1.28308.2.1.1', '1', 'communityIndex', 'td_communityManagement', 'communityIndex, id', 'OctetString', '0', '1', 'mandatory', '1.3.6.1.4.1.28308.2.1.2' );

INSERT INTO tc_communityManagement VALUES ( '1.3.6.1.4.1.28308.2.1.2', '2', 'communityName', 'td_communityManagement', 'communityIndex, id', 'OctetString', '0', '1', 'mandatory', '1.3.6.1.4.1.28308.2.1.3' );

INSERT INTO tc_communityManagement VALUES ( '1.3.6.1.4.1.28308.2.1.3', '3', 'id', 'td_communityManagement', 'communityIndex, id', 'INTEGER', '0', '1', 'mandatory', '1.3.6.1.4.1.28308.2.1.4' );

INSERT INTO tc_communityManagement VALUES ( '1.3.6.1.4.1.28308.2.1.4', '4', 'access', 'td_communityManagement', 'communityIndex, id', 'INTEGER', '0', '3', 'mandatory', '1.3.6.1.4.1.28308.2.1.5' );

INSERT INTO tc_communityManagement VALUES ( '1.3.6.1.4.1.28308.2.1.5', '5', 'view', 'td_communityManagement', 'communityIndex, id', 'OID', '0', '3', 'mandatory', '1.3.6.1.4.1.28308.2.1.6' );

INSERT INTO tc_communityManagement VALUES ( '1.3.6.1.4.1.28308.2.1.6', '6', 'communityStatus', 'td_communityManagement', 'communityIndex, id', 'INTEGER', '0', '3', 'mandatory', '1.3.6.1.4.1.28309' );



-- TABLA td_comunidades

CREATE TABLE td_communityManagement ( communityIndex TEXT, communityName TEXT, id INT, access INT(2) DEFAULT 0, view VARCHAR(255) DEFAULT '1.3', communityStatus INT(2) );


-- Creamos los usuarios con permiso de acceso remoto

GRANT ALL ON rmon.* TO 'rmon'@'localhost' IDENTIFIED BY 'rmon';
GRANT ALL ON comunidades.* TO 'rmon'@'localhost' IDENTIFIED BY 'rmon';
