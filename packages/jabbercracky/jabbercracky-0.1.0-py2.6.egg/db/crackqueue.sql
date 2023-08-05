--
-- Table structure for table `queue`
--

DROP TABLE IF EXISTS `queue`;

CREATE TABLE `queue` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `state` int(10) unsigned NOT NULL default '0',
  `type` varchar(45) NOT NULL,
  `src_ip` varchar(45) NOT NULL,
  `hash` varchar(45) NOT NULL,
  `clear` varchar(45) default NULL,
  `created` datetime NOT NULL,
  `cracked` datetime default NULL,
  `started` datetime default NULL,
  `maxcpu` int(11) default NULL,
  `threads` int(11) default NULL,
  `lastpw` varchar(45) default '',
  PRIMARY KEY  (`id`)
);

