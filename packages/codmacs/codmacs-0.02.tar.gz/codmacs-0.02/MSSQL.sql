<tables>
select name from dbo.sysobjects
where OBJECTPROPERTY(id, N'IsUserTable') = 1
and status>0
order by name
</tables>

<columns>
SELECT name,colorder,dtype,nullable,length,otro,(CASE WHEN pkey is null then '' else 'PRI' END) AS pkey,come
FROM(
select c.name,c.colorder,
t.name AS dtype,(CASE WHEN c.isnullable=1 THEN 'YES' ELSE 'NO' END) AS nullable,
c.length,-1 as otro,
(SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE OBJECTPROPERTY(OBJECT_ID(constraint_name), 'IsPrimaryKey') = 1
AND column_name=c.name
AND table_name = '$stabl') AS pkey,
'' AS come
from dbo.syscolumns AS c
left join dbo.systypes as t on t.xtype=c.xtype and t.usertype=c.usertype
Where c.id=(select id from dbo.sysobjects where name='$stabl')
) AS tmp
order by colorder
</columns>