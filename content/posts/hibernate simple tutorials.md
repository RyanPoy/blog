+++
title = "Hibernate入门使用"
date = "2008-07-24"

categories = ["Tutorials"]
tags = ["Java", "Hibernate"]
+++

Hibernate入门使用文章, 主要讲快速使用，不会介绍太多的深层次的东西。方便自己，方便大家。因本人懒惰，记不住hibernate的配置选项，所以，此文实例都是使用myeclipse进行快速开发，数据库都是mysql。

<!--more-->

## 初次使用
直接上需求：实现对用户的增、删、改、查。

为了方便，用户就2个属性 用户ID和用户名。实体模型如下：

![Imgurl](/images/hibernate-1.gif)

建立工程:HibernateQuickUse，并且建立包。如下：

![Imgurl](/images/hibernate-2.gif)

### Pojo
根据实体，创建类User，代码如下：

```java
@SuppressWarnings("serial")
public class User implements java.io.Serializable {
	private String id;
	private String name;
	public User() { }
	public String getId() { return this.id; }   
	public void setId(String id) { this.id = id; }  
	public String getName() { return this.name; }
	public void setName(String name) {this.name = name;}
}
```

### DB
根据实体，创建数据表。sql如下：

```sql
use HibernateQuickUse;
drop table if exists User;
create table user (
	id varchar(32) primary key,
	name varchar(32)
);
```

这里的id，我没有采用Integer auto_increment, 原因是为了数据库的数据能方便的导入到另外一种数据库里面，比方说：oracle。当然，这个是以牺牲部分效率为前提的。因为id是integer的，能更加快速查询。不过，从数据库会自动为 primary key 建立 index来看，效率也不会相差太多。

### hibernate.cfg.xml
要想通过hibernate访问数据库。首先要建立描述数据库的文件：hibernate.cfg.xml。放到src下面。内容如下：

```xml
<!DOCTYPE hibernate-configuration PUBLIC  
			"-//Hibernate/Hibernate Configuration DTD 3.0//EN"  
			"http://hibernate.sourceforge.net/hibernate-configuration-3.0.dtd">  
<hibernate-configuration>  
	<session-factory> 
		<!-- dialect, 这个对应着hibernate生成哪种数据库的sql。-->
		<property name="dialect">org.hibernate.dialect.MySQLDialect</property>  
		<property name="connection.url">jdbc:mysql://localhost:3306/hibernatequickUse</property>  
		<property name="connection.username">root</property>  
		<property name="connection.password">root</property>  
		<property name="connection.driver_class">com.mysql.jdbc.Driver</property>  
		<!-- show_sql, 这个是为了调试时候输出sql语句到屏幕用 -->
		<property name="show_sql">true</property>  
		<mapping resource="org/py/hib/quickstart/User.hbm.xml" />  
	</session-factory>  
</hibernate-configuration>
```

### User.hbm.xml
实体-数据库映射文件 -- 主要是告诉hibernate，这个User类，对应着哪个table，User类里面的那个属性对应着table里面的哪个字段。

我们可以建立 实体-数据库 的xml映射文件，也可以采用Annotations映射，但是目前只说xml映射方式。如下：
```xml
<?xml version="1.0" encoding="utf-8"?>  
<!DOCTYPE hibernate-mapping PUBLIC "-//Hibernate/Hibernate Mapping DTD 3.0//EN"  
	"http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">  
<hibernate-mapping>  
	<class name="org.py.hib.quickstart.User" table="user">  
		<id name="id" type="java.lang.String" column="id" length="32">  
			<!-- id的生成策略采用 uuid，也可以是 native等 -->
			<generator class="uuid" />  
		</id>
		<property name="name"  type="java.lang.String" column="name" length="32" />  
	</class>
</hibernate-mapping>
```

### Testing
有了上面的准备，那么我们开始来用junit测试.
我把测试用力放到了test/org.py.hib.quickstart下面。代码如下：
```java
import junit.framework.Assert;
import junit.framework.TestCase;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;
import org.junit.After;
import org.junit.Before;

public class QuickStartTest extends TestCase {
    SessionFactory factory;
    String m_name = "ryanpoy";
    String m_name2 = "ryanpoy2";

    @Before
    public void setUp() throws Exception {
        Configuration conf = new Configuration().configure();
        factory = conf.buildSessionFactory();
    }

    public void testSave() throws Exception {
        System.out.println("\n=== test save ===");
        User u = new User();
        u.setName(m_name); // 设置用户名 = m_name

        Session session = null;
        Transaction tran = null;
        try {
            session = factory.openSession();
            tran = session.beginTransaction();
            session.save(u);
            tran.commit();

            Assert.assertEquals(u.getId() != null, true);
        } catch (Exception ex) {
            tran.rollback();
            throw ex;
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (Exception ex) {
                    // nothing to do
                } finally {
                    if (session != null)
                        session = null;
                }
            }
        }
    }

    public void testFind() throws Exception {
        System.out.println("=== test find ===");
        Session session = null;
        try {
            session = factory.openSession();
            User u = (User) session.createQuery(" from User").list().get(0);

            Assert.assertEquals(true, u.getId() != null);
            Assert.assertEquals(m_name, u.getName());
        } catch (Exception ex) {
            throw ex;
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (Exception ex) {
                    // nothing to do
                } finally {
                    if (session != null)
                        session = null;
                }
            }
        }
    }

    public void testModify() throws Exception {
        System.out.println("\n=== test modify ===");
        Session session = null;
        Transaction tran = null;
        try {
            session = factory.openSession();
            tran = session.beginTransaction();
            User u = (User) session.createQuery(" from User").list().get(0);
            u.setName(m_name2);  // 修改用户名 = m_name2.（原来用户名= m_name）
            tran.commit();

        } catch (Exception ex) {
            throw ex;
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (Exception ex) {
                    // nothing to do
                } finally {
                    if (session != null)
                        session = null;
                }
            }
        }

        /*
         * 修改后再查询
         */
        System.out.println("\n=== test find after modify ===");
        try {
            session = factory.openSession();
            User u = (User) session.createQuery(" from User").list().get(0);

            Assert.assertEquals(true, u.getId() != null);
            Assert.assertEquals(m_name2, u.getName());
        } catch (Exception ex) {
            throw ex;
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (Exception ex) {
                    // nothing to do
                } finally {
                    if (session != null)
                        session = null;
                }
            }
        }
    }

    public void testDelete() throws Exception {
        System.out.println("\n=== test delete ===");
        Session session = null;
        Transaction tran = null;
        try {
            session = factory.openSession();
            tran = session.beginTransaction();

            User u = (User) session.createQuery(" from User").list().get(0);
            session.delete(u);
            tran.commit();

        } catch (Exception ex) {
            throw ex;
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (Exception ex) {
                    // nothing to do
                } finally {
                    if (session != null)
                        session = null;
                }
            }
        }

        /*
         * 删除后再查询
         */
        System.out.println("\n=== test find after delete ===");
        try {
            session = factory.openSession();
            Integer num = (Integer) session.createQuery(" from User").list().size();

            Assert.assertEquals(0, num.intValue());
        } catch (Exception ex) {
            throw ex;
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (Exception ex) {
                    // nothing to do
                } finally {
                    if (session != null)
                        session = null;
                }
            }
        }
    }

    @After
    public void tearDown() throws Exception {
        factory.close();
    }
}
```
运行后，我们很欣慰的看到一路绿灯，全部通过了。那么测试没有问题。呵呵(这里的测试可能还不完善。请大家指出。前面说过，我对测试这块也不熟)。

看控制台，会输出如下信息：
```sql
=== test save ===
Hibernate: insert into hibernatequickuse.user (name, id) values (?, ?)

=== test find ===
Hibernate: select user0_.id as id2_, user0_.name as name2_ from hibernatequickuse.user user0_

=== test modify ===
Hibernate: select user0_.id as id4_, user0_.name as name4_ from hibernatequickuse.user user0_
Hibernate: update hibernatequickuse.user set name=? where id=?

=== test find after modify ===
Hibernate: select user0_.id as id4_, user0_.name as name4_ from hibernatequickuse.user user0_

=== test delete ===
Hibernate: select user0_.id as id6_, user0_.name as name6_ from hibernatequickuse.user user0_
Hibernate: delete from hibernatequickuse.user where id=?

=== test find after delete ===
Hibernate: select user0_.id as id6_, user0_.name as name6_ from hibernatequickuse.user user0_
```
这些，就是hibernte自动生成的。仔细看看，其实就是标准sql。呵呵。懂jdbc的都能看懂。


## xml关系映射 1:1
1对1的关系在现实中很常见。比方说：人和身份证。1个身份证对应着一个身份证，一个身份证对应着一个人。那么，我们就以此为原型。进行代码编写。

实体模型

![1对1实体模型](/images/hibernate-3.gif)

### DB
根据模型，创建数据库：
```sql
use HibernateQuickUse;
drop table if exists Person;
drop table if exists Card;

create table Card (
	id varchar(32) primary key,
	cardDesc varchar(128) not null
);

create table Person (
	id varchar(32) primary key,
	name varchar(32) not null,
	card_id varchar(32) not null,
	foreign key(card_id) references Card(id)
);
```

### Pojo
java代码如下：

Person类

```java

@SuppressWarnings("serial")
public class Person implements java.io.Serializable {
	private String id;
	private String name;
	private Card card;

	public Person() { }

	public String getId() { return this.id; }
	public void setId(String id) { this.id = id; }

	public Card getCard() {return this.card;}
	public void setCard(Card card) { this.card = card; }

	public String getName() { return this.name; }
	public void setName(String name) { this.name = name; }
}
```

Card类：
```java
@SuppressWarnings("serial")
public class Card implements java.io.Serializable
{
	private String id;

	private String cardDesc;

	public Card() { }

	public String getId() { return this.id; }
	public void setId(String id) { this.id = id; }

	public String getCardDesc() { return cardDesc; }
	public void setCardDesc(String cardDesc) { this.cardDesc = cardDesc; }
}
```

### Mapping Xml
xml映射文件如下：

Person.hbm.xml
```xml
<?xml version="1.0" encoding="utf-8"?>  
<!DOCTYPE hibernate-mapping PUBLIC "-//Hibernate/Hibernate Mapping DTD 3.0//EN"  
	"http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">  
	
<hibernate-mapping>  
	<class name="org.py.hib.relation.one2one.Person" table="person">  
		<id name="id" type="java.lang.String" column="id" length="32">  
			<generator class="uuid" />  
		</id>  
	
		<property name="name" type="java.lang.String">  
			<column name="name" length="32" />  
		</property>  
	
		<many-to-one name="card" class="org.py.hib.relation.one2one.Card" unique="true"  
			cascade="all" column="card_id" />  
				
	</class>  
</hibernate-mapping>
```

今天讲的是one-to-one配置。但是，此处用的是many-to-one，这个是什么原因呢？其实，one-to-one就是特殊的many-to-one。

Card.hbm.xml：
```xml
<?xml version="1.0" encoding="utf-8"?>  
<!DOCTYPE hibernate-mapping PUBLIC "-//Hibernate/Hibernate Mapping DTD 3.0//EN"  
	"http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">  

<hibernate-mapping>  
	<class name="org.py.hib.relation.one2one.Card" table="card">  
		<id name="id" type="java.lang.String" column="id" length="32">  
			<generator class="uuid" />  
		</id>  
			
		<property name="cardDesc" type="java.lang.String" column="cardDesc" length="128" not-null="true"/>  
	
	</class>  
</hibernate-mapping> 
```

### Testing
测试代码如下：

One2OneTest.java

```java    
import junit.framework.Assert;
import junit.framework.TestCase;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;
import org.junit.After;
import org.junit.Before;

public class One2OneTest extends TestCase {
	private SessionFactory factory;
	private String m_name = "ryanpoy";
	private String m_name2 = "ryanpoy2";
	private String m_cardDesc1 = "desc_1";
	private String m_cardDesc2 = "desc_2";

	@Before
	public void setUp() throws Exception {
		Configuration conf = new Configuration().configure();
		factory = conf.buildSessionFactory();
	}

	public void testSave() throws Exception {
		System.out.println("\n=== test save ===");

		Card card = new Card();
		card.setCardDesc(m_cardDesc1);

		Person person = new Person();
		person.setName(m_name); // 设置用户名 = m_name
		person.setCard(card);

		Session session = null;
		Transaction tran = null;
		try {
			session = factory.openSession();
			
			tran = session.beginTransaction();
			session.save(person);
			tran.commit();

			Assert.assertEquals(person.getId() != null, true);
			Assert.assertEquals(card.getId() != null, true);
		} catch (Exception ex) {
			tran.rollback();
			throw ex;
		} finally {
			if (session != null) {
				try {
					session.close();
				} catch (Exception ex) {
					// nothing to do
				} finally {
					if (session != null)
						session = null;
				}
			}
		}
	}

    public void testFind() throws Exception {
		System.out.println("\n=== test find ===");
		Session session = null;
		try {
			session = factory.openSession();
			Person person = (Person) session.createQuery("from Person").list().get(0);

			Assert.assertEquals(true, person.getId() != null);
			Assert.assertEquals(m_name, person.getName());

			Assert.assertEquals(true, person.getCard().getId() != null);
			Assert.assertEquals(m_cardDesc1, person.getCard().getCardDesc());

		} catch (Exception ex) {
			throw ex;
		} finally {
			if (session != null) {
				try {
					session.close();
				} catch (Exception ex) {
					// nothing to do
				} finally {
					if (session != null)
						session = null;
				}
			}
		}
	}

    public void testModify() throws Exception {
		System.out.println("\n=== test modify ===");
		Session session = null;
		Transaction tran = null;
		try {
			session = factory.openSession();
			tran = session.beginTransaction();

			Person person = (Person) session.createQuery("from Person").list().get(0);
			person.setName(m_name2); // 修改用户名 = m_name2.（原来用户名= m_name）
			person.getCard().setCardDesc(m_cardDesc2); // 修改cardDesc 为 m_cardDesc2 (原来是：m_cardDesc1)
			tran.commit();

		} catch (Exception ex) {
			throw ex;
		} finally {
			if (session != null) {
				try {
					session.close();
				} catch (Exception ex) {
					// nothing to do
				} finally {
					if (session != null)
						session = null;
				}
			}
		}
   
		System.out.println("\n=== test find after modify ===");
		try {
			session = factory.openSession();
			Person person = (Person) session.createQuery("from Person").list().get(0);

			Assert.assertEquals(true, person.getId() != null);
			Assert.assertEquals(m_name2, person.getName());

			Assert.assertEquals(true, person.getCard().getId() != null);
			Assert.assertEquals(m_cardDesc2, person.getCard().getCardDesc());

		} catch (Exception ex) {
			throw ex;
		} finally {
			if (session != null) {
				try {
					session.close();
				} catch (Exception ex) {
					// nothing to do
				} finally {
					if (session != null)
						session = null;
				}
			}
		}
	}

	
    public void testDelete() throws Exception {
		System.out.println("\n=== test delete ===");
		Session session = null;
		Transaction tran = null;
		try {
			session = factory.openSession();
			tran = session.beginTransaction();

			Person person = (Person) session.createQuery("from Person").list().get(0);
			session.delete(person);
			tran.commit();
		} catch (Exception ex) {
			throw ex;
		} finally {
			if (session != null) {
				try {
					session.close();
				} catch (Exception ex) {
					// nothing to do
				} finally {
					if (session != null)
						session = null;
				}
			}
		}

		/*
		 * 删除后再查询
		 */
		System.out.println("\n=== test find after delete ===");
		try {
			session = factory.openSession();

			Integer num = (Integer) session.createQuery("from Person").list().size();
			Assert.assertEquals(0, num.intValue());

			num = (Integer) session.createQuery("from Card").list().size();
			Assert.assertEquals(0, num.intValue());

		} catch (Exception ex) {
			throw ex;
		} finally {
			if (session != null) {
				try {
					session.close();
				} catch (Exception ex) {
					// nothing to do
				} finally {
					if (session != null)
						session = null;
				}
			}
		}
	}

	@After
	public void tearDown() throws Exception {
		factory.close();
	}

}
```

运行test，一路飚绿。呵呵。陶醉一番。不过，这也就是一个拿不出手的测试和一个拿不出手的例子。没有任何实际意义的例子。仅此一个demo而已。

在1：1中，其实还有一种方式，即：唯一主见关联。但是，我一直倾向于上面的这种形式，所以，唯一主见关联的就不再介绍了。


## xml关系映射 1:n
因为n:1就是1:1，两者是一样的，所以不单独说了。下面主要讲主要讲1:n：

这次用到的例子是Father和child之间的关系。一个father可以有n个child，但是1个child只有一个father。这里只说生父。至于其他的继父、养父、干爹等等，不再范围之内。

建立实体模型如下：

![One2Many](/images/hibernate-4.gif)
 
### DB 
根据模型创建数据库。sql脚本如下：
```sql
use HibernateQuickUse;
drop table if exists Child;
drop table if exists Father;

create table Father (
	id varchar(32) primary key,
	name varchar(32) not null
);

create table Child (
	id varchar(32) primary key,
	name varchar(128) not null,
	father_id varchar(32) not null,
	foreign key(father_id) references Father(id)
);
```

### Pojo
根据模型创建java对象。

Father.java：
```java
import java.util.HashSet;
import java.util.Set;

@SuppressWarnings("serial")
public class Father implements java.io.Serializable
{
	private String id;
	private String name;
	private Set children = new HashSet(0);

	public String getId() { return this.id; }
	public void setId(String id) { this.id = id; }

	public String getName() { return this.name; }
	public void setName(String name) { this.name = name; }

	public Set getChildren() { return children; }
	public void setChildren(Set children) { this.children = children; }
}
```

Child.java：
```java

@SuppressWarnings("serial")
public class Child implements java.io.Serializable
{
	private String id;
	private String name;
	private Father father;

	public String getId() { return this.id; }
	public void setId(String id) { this.id = id; }

	public Father getFather() { return this.father; }
	public void setFather(Father father) { this.father = father; }
	
	public String getName() { return this.name; }
	public void setName(String name) { this.name = name;}
}
```

### Mapping Xml
映射文件如下：

Father.hbm.xml：
```xml
<?xml version="1.0" encoding="utf-8"?>  
<!DOCTYPE hibernate-mapping PUBLIC "-//Hibernate/Hibernate Mapping DTD 3.0//EN"  
	"http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">  
	
<hibernate-mapping>  
	<class name="org.py.hib.relation.one2many.Father" table="father">  
		<id name="id" type="java.lang.String" column="id" length="32">  
			<generator class="uuid" />  
		</id>  
	
		<property name="name" type="java.lang.String" column="name" length="32" not-null="true"/>  
			
		<set name="children" table="child" cascade="all" inverse="true">  
			<key column="father_id" />  
			<one-to-many class="org.py.hib.relation.one2many.Child" />  
		</set>  
	</class>  
</hibernate-mapping> 
```

这里要说说 "set" 这个标签里面的内容。

1. "name"是Father里面的属性的名字。
1. "table"表示它对应的是数据库中的哪个表。
1. cascade="all" 表示所有的操作都级联操作。
1. "inverse"表示关系的维护由谁来执行。
    > true表示不由自己执行，而有对应的另外一方执行。
    > false则相反，表示由自己维护关系。
    > 这里设置成 true 是由原因的。如果说把它设置成为false，那么就由他来维护关系了。

**这里得说一下inverse属性的问题**。在one-to-many中，如果关系由one来维护，那么会很麻烦，性能也会很低。每次对many一方的一条记录进行增、删、改 时都会多一次update操作。原因很简单，因为关系的维护设置在了one这一方，所以对many的每一次操作，one这一方都要维护一次双方的关系。

这个就好像皇帝和老百姓的关系。试问，是来一个老百姓，皇帝就宣布他是我的子民，还是由老百姓直接选择做那个皇帝的子民更加有效率呢？呵呵。不知道这个例子大家有没有明白。关于inverse的更具体的说明，在javaeye上搜一下，就会发现有很多。这里推荐一篇，我认为讲得很明白的： [inverse](http://www.iteye.com/topic/156289)  

"key" 中的 "column" 表示在table(这里的table是child)中, 跟Father关联的字段名称。这里是"father_id"。可以看看开始的sql脚本。

one-to-many 表示father和children的关系。class则表示是同哪个类是这种关系。

Child.hbm.xml：

```xml
<?xml version="1.0" encoding="utf-8"?>  
<!DOCTYPE hibernate-mapping PUBLIC "-//Hibernate/Hibernate Mapping DTD 3.0//EN"  
	"http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">  
	
<hibernate-mapping>  
	<class name="org.py.hib.relation.one2many.Child" table="child">  
		<id name="id" type="java.lang.String" column="id" length="32" >  
			<generator class="uuid" />  
		</id>  
		<property name="name" type="java.lang.String" column="name" length="128" not-null="true"/>  
	
		<many-to-one name="father" class="org.py.hib.relation.one2many.Father" column="father_id" />  
	</class>  
</hibernate-mapping> 
```
这个里面主要就是多了一个many-to-one，表示child 和 father 的关系是"many-to-one"


### Testing

测试代码如下：

One2ManyTest.java
```java
import java.util.Set;

import junit.framework.Assert;
import junit.framework.TestCase;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;
import org.junit.After;
import org.junit.Before;

public class One2ManyTest extends TestCase {
    private SessionFactory factory;
    private static final String[] childname = new String[]{"child_1", "child_2", "child_3"};
    private static final String[] newchildname = new String[]{"new_child_1", "new_child_2", "new_child_3"};

    @Before
    public void setUp() throws Exception {
        Configuration conf = new Configuration().configure();
        factory = conf.buildSessionFactory();
    }


    public void testSave() throws Exception {
        System.out.println("\n=== test save ===");

        Father father = new Father();
        father.setName("Father_1");

        Child child1 = new Child();
        child1.setName(childname[0]);

        Child child2 = new Child();
        child2.setName(childname[1]);

        Child child3 = new Child();
        child3.setName(childname[2]);

        father.getChildren().add(child1);
        father.getChildren().add(child2);
        father.getChildren().add(child3);

        child1.setFather(father);
        child2.setFather(father);
        child3.setFather(father);

        Session session = null;
        Transaction tran = null;
        try {
            session = factory.openSession();
            tran = session.beginTransaction();
            session.save(father);

            tran.commit();

            Assert.assertNotNull(father.getId());

            Assert.assertNotNull(child1.getId());
            Assert.assertNotNull(child2.getId());
            Assert.assertNotNull(child3.getId());

        } catch (Exception ex) {
            tran.rollback();
            throw ex;
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (Exception ex) {
                    // nothing to do
                } finally {
                    if (session != null)
                        session = null;
                }
            }
        }
    }

    private boolean isChildrenName(String name) {
        for (String n : childname) {
            if (n.equals(name))
                return true;
        }

        return false;
    }

    private boolean isNewChildrenName(String name) {
        for (String n : newchildname) {
            if (n.equals(name))
                return true;
        }

        return false;
    }

    public void testFind() throws Exception {
        System.out.println("\n=== test find ===");
        Session session = null;
        try {
            session = factory.openSession();
            Father father = (Father) session.createQuery("from Father").list().get(0);

            Assert.assertNotNull(father.getId());
            Assert.assertEquals("Father_1", father.getName());

            Set children = father.getChildren();
            for (Child child : children) {
                Assert.assertEquals(child.getFather(), father);

                Assert.assertNotNull(child.getId());

                Assert.assertTrue(isChildrenName(child.getName()));
            }
        } catch (Exception ex) {
            throw ex;
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (Exception ex) {
                    // nothing to do
                } finally {
                    if (session != null)
                        session = null;
                }
            }
        }
    }

    public void testModify() throws Exception {
        System.out.println("\n=== test modify ===");
        Session session = null;
        Transaction tran = null;
        try {
            session = factory.openSession();
            tran = session.beginTransaction();

            Father father = (Father) session.createQuery("from Father").list().get(0);
            father.setName("Father_2"); // 修改用户名 = m_name2.（原来用户名= m_name）

            Set children = father.getChildren();
            int i = 0;
            for (Child child : children) {
                child.setName(newchildname[i++]);
            }

            tran.commit();

        } catch (Exception ex) {
            throw ex;
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (Exception ex) {
                    // nothing to do
                } finally {
                    if (session != null)
                        session = null;
                }
            }
        }

        /*
         * 修改后再查询
         */
        System.out.println("\n=== test find after modify ===");
        try {
            session = factory.openSession();
            Father father = (Father) session.createQuery("from Father").list().get(0);

            Assert.assertNotNull(father.getId());
            Assert.assertEquals("Father_2", father.getName());

            Set children = father.getChildren();

            for (Child child : children) {
                Assert.assertEquals(child.getFather(), father);

                Assert.assertNotNull(child.getId());

                Assert.assertTrue(isNewChildrenName(child.getName()));
            }

        } catch (Exception ex) {
            throw ex;
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (Exception ex) {
                    // nothing to do
                } finally {
                    if (session != null)
                        session = null;
                }
            }
        }
    }

    public void testDelete() throws Exception {
        System.out.println("\n=== test delete ===");
        Session session = null;
        Transaction tran = null;
        try {
            session = factory.openSession();
            tran = session.beginTransaction();

            Father father = (Father) session.createQuery("from Father").list().get(0);
            session.delete(father);
            tran.commit();

        } catch (Exception ex) {
            throw ex;
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (Exception ex) {
                    // nothing to do
                } finally {
                    if (session != null)
                        session = null;
                }
            }
        }

        /*
         * 删除后再查询
         */
        System.out.println("\n=== test find after delete ===");
        try {
            session = factory.openSession();

            Integer num = (Integer) session.createQuery("from Father").list().size();
            Assert.assertEquals(0, num.intValue());

            num = (Integer) session.createQuery("from Child").list().size();
            Assert.assertEquals(0, num.intValue());

        } catch (Exception ex) {
            throw ex;
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (Exception ex) {
                    // nothing to do
                } finally {
                    if (session != null)
                        session = null;
                }
            }
        }
    }

    @After
    public void tearDown() throws Exception {
        factory.close();
    }
}
```

这里不得不再重申以下 one-to-many 中 inverse 关系的维护问题。 在one-to-many中，把inverse放到many中来维护是一个好的习惯。大家可以把上面的inverse改成false，看看会发生什么情况。

在inverse=true的时候，输出结果如下：
```sql
=== test save ===
Hibernate: insert into father (name, id) values (?, ?)
Hibernate: insert into child (name, father_id, id) values (?, ?, ?)
Hibernate: insert into child (name, father_id, id) values (?, ?, ?)
Hibernate: insert into child (name, father_id, id) values (?, ?, ?)

=== test find ===
Hibernate: select father0_.id as id13_, father0_.name as name13_ from father father0_
Hibernate: select children0_.father_id as father3_1_, children0_.id as id1_, children0_.id as id14_0_, children0_.name as name14_0_, children0_.father_id as father3_14_0_ from child children0_ where children0_.father_id=?

=== test modify ===
Hibernate: select father0_.id as id23_, father0_.name as name23_ from father father0_
Hibernate: select children0_.father_id as father3_1_, children0_.id as id1_, children0_.id as id24_0_, children0_.name as name24_0_, children0_.father_id as father3_24_0_ from child children0_ where children0_.father_id=?
Hibernate: update father set name=? where id=?
Hibernate: update child set name=?, father_id=? where id=?
Hibernate: update child set name=?, father_id=? where id=?
Hibernate: update child set name=?, father_id=? where id=?

=== test find after modify ===
Hibernate: select father0_.id as id23_, father0_.name as name23_ from father father0_
Hibernate: select children0_.father_id as father3_1_, children0_.id as id1_, children0_.id as id24_0_, children0_.name as name24_0_, children0_.father_id as father3_24_0_ from child children0_ where children0_.father_id=?

=== test delete ===
Hibernate: select father0_.id as id33_, father0_.name as name33_ from father father0_
Hibernate: select children0_.father_id as father3_1_, children0_.id as id1_, children0_.id as id34_0_, children0_.name as name34_0_, children0_.father_id as father3_34_0_ from child children0_ where children0_.father_id=?
Hibernate: delete from child where id=?
Hibernate: delete from child where id=?
Hibernate: delete from child where id=?
Hibernate: delete from father where id=?

=== test find after delete ===
Hibernate: select father0_.id as id33_, father0_.name as name33_ from father father0_
Hibernate: select child0_.id as id34_, child0_.name as name34_, child0_.father_id as father3_34_ from child child0_
```

而改成**inverse=false**后，testDelete()是没法通过的。输出如下：

```sql
log4j:WARN No appenders could be found for logger (org.hibernate.cfg.Environment).
log4j:WARN Please initialize the log4j system properly.

=== test save ===
Hibernate: insert into father (name, id) values (?, ?)
Hibernate: insert into child (name, father_id, id) values (?, ?, ?)
Hibernate: insert into child (name, father_id, id) values (?, ?, ?)
Hibernate: insert into child (name, father_id, id) values (?, ?, ?)
Hibernate: update child set father_id=? where id=?
Hibernate: update child set father_id=? where id=?
Hibernate: update child set father_id=? where id=?

=== test find ===
Hibernate: select father0_.id as id13_, father0_.name as name13_ from father father0_
Hibernate: select children0_.father_id as father3_1_, children0_.id as id1_, children0_.id as id14_0_, children0_.name as name14_0_, children0_.father_id as father3_14_0_ from child children0_ where children0_.father_id=?

=== test modify ===
Hibernate: select father0_.id as id23_, father0_.name as name23_ from father father0_
Hibernate: select children0_.father_id as father3_1_, children0_.id as id1_, children0_.id as id24_0_, children0_.name as name24_0_, children0_.father_id as father3_24_0_ from child children0_ where children0_.father_id=?
Hibernate: update father set name=? where id=?
Hibernate: update child set name=?, father_id=? where id=?
Hibernate: update child set name=?, father_id=? where id=?
Hibernate: update child set name=?, father_id=? where id=?

=== test find after modify ===
Hibernate: select father0_.id as id23_, father0_.name as name23_ from father father0_
Hibernate: select children0_.father_id as father3_1_, children0_.id as id1_, children0_.id as id24_0_, children0_.name as name24_0_, children0_.father_id as father3_24_0_ from child children0_ where children0_.father_id=?

=== test delete ===
Hibernate: select father0_.id as id33_, father0_.name as name33_ from father father0_
Hibernate: select children0_.father_id as father3_1_, children0_.id as id1_, children0_.id as id34_0_, children0_.name as name34_0_, children0_.father_id as father3_34_0_ from child children0_ where children0_.father_id=?
Hibernate: update child set father_id=null where father_id=?
```

产生了错误，原因是：违反了非空约束。

得修改sql脚本，把Child的建表脚本中的：
```sql
father_id varchar(32) not null, 
```

修改成为：
```
father_id varchar(32),
```
才能通过。这个时候输出的结果是：
```sql
log4j:WARN No appenders could be found for logger (org.hibernate.cfg.Environment).
log4j:WARN Please initialize the log4j system properly.

=== test save ===
Hibernate: insert into father (name, id) values (?, ?)
Hibernate: insert into child (name, father_id, id) values (?, ?, ?)
Hibernate: insert into child (name, father_id, id) values (?, ?, ?)
Hibernate: insert into child (name, father_id, id) values (?, ?, ?)
Hibernate: update child set father_id=? where id=?
Hibernate: update child set father_id=? where id=?
Hibernate: update child set father_id=? where id=?

=== test find ===
Hibernate: select father0_.id as id13_, father0_.name as name13_ from father father0_
Hibernate: select children0_.father_id as father3_1_, children0_.id as id1_, children0_.id as id14_0_, children0_.name as name14_0_, children0_.father_id as father3_14_0_ from child children0_ where children0_.father_id=?

=== test modify ===
Hibernate: select father0_.id as id23_, father0_.name as name23_ from father father0_
Hibernate: select children0_.father_id as father3_1_, children0_.id as id1_, children0_.id as id24_0_, children0_.name as name24_0_, children0_.father_id as father3_24_0_ from child children0_ where children0_.father_id=?
Hibernate: update father set name=? where id=?
Hibernate: update child set name=?, father_id=? where id=?
Hibernate: update child set name=?, father_id=? where id=?
Hibernate: update child set name=?, father_id=? where id=?

=== test find after modify ===
Hibernate: select father0_.id as id23_, father0_.name as name23_ from father father0_
Hibernate: select children0_.father_id as father3_1_, children0_.id as id1_, children0_.id as id24_0_, children0_.name as name24_0_, children0_.father_id as father3_24_0_ from child children0_ where children0_.father_id=?

=== test delete ===
Hibernate: select father0_.id as id33_, father0_.name as name33_ from father father0_
Hibernate: select children0_.father_id as father3_1_, children0_.id as id1_, children0_.id as id34_0_, children0_.name as name34_0_, children0_.father_id as father3_34_0_ from child children0_ where children0_.father_id=?
Hibernate: update child set father_id=null where father_id=?
Hibernate: delete from child where id=?
Hibernate: delete from child where id=?
Hibernate: delete from child where id=?
Hibernate: delete from father where id=?

=== test find after delete ===
Hibernate: select father0_.id as id33_, father0_.name as name33_ from father father0_
Hibernate: select child0_.id as id34_, child0_.name as name34_, child0_.father_id as father3_34_ from child child0_
```

所以，**inverse的设置是很重要的一个事情。**

## xml关系映射 n:n

我们以老师和学生为例，一个老师可以交很多学生，同样一个学生可以拥有多个老师，所以，他们之间的关系就是n：n的。

实体模型：
![many2many](/images/hibernate-5.gif)

从实体模型来看。有2个对象，但是为了在数据库中表示出2者的n:n的关系，我们还得引入一张表。

### DB
sql脚本如下：
```sql
use HibernateQuickUse;
drop table if exists teacher_student_relation;
drop table if exists Teacher;
drop table if exists Student;

create table Teacher (
	tid varchar(32) primary key,
	name varchar(32) not null
);

create table Student (
	sid varchar(32) primary key,
	name varchar(128) not null
);

create table teacher_student_relation (
	id integer auto_increment primary key,
	teacher_id varchar(32) not null,
	student_id varchar(32) not null,
	foreign key(teacher_id) references Teacher(tid),
	foreign key(student_id) references Student(sid)
);
```
 
### Pojo
通过模型，创建java类如下：

Student.java
```java
import java.util.HashSet;
import java.util.Set;

@SuppressWarnings("serial")
public class Student implements java.io.Serializable {
	private String id;
	private String name;
	private Set teachers = new HashSet(0);

	public Student() {}

	public String getId() {return this.id;}
	public void setId(String id) {this.id = id;}

	public String getName() {return this.name;}
	public void setName(String name) {this.name = name;}

	public Set getTeachers() {return teachers;}
	public void setTeachers(Set teachers) {this.teachers = teachers;}
}
```
 
Teacher.java:

```java
import java.util.HashSet;
import java.util.Set;

@SuppressWarnings("serial")
public class Teacher implements java.io.Serializable {
	private String id;
	private String name;
	private Set students = new HashSet(0);

	public Teacher() {}

	public String getId() { return this.id;}
	public void setId(String id) { this.id = id;}

	public String getName() { return this.name;}
	public void setName(String name) { this.name = name;}
	
	public Set getStudents() { return students;}
	public void setStudents(Set students) { this.students = students;}
}
```

### Mapping Xml
xml映射文件如下

Student.hbm.xml
```xml
<?xml version="1.0" encoding="utf-8"?>  
<!DOCTYPE hibernate-mapping PUBLIC "-//Hibernate/Hibernate Mapping DTD 3.0//EN"  
	"http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">  
	
<hibernate-mapping>  
	<class name="org.py.hib.relation.many2many.Student"  
		table="student">  
		<id name="id" type="java.lang.String" column="sid" length="32">  
			<generator class="uuid" />  
		</id>  
	
		<property name="name" type="java.lang.String" column="name"  
			length="128" not-null="true" />  
	
		<set name="teachers" table="teacher_student_relation" cascade="save-update" inverse="false">  
			<key column="student_id" not-null="true" />  
	
			<many-to-many column="teacher_id"  
				class="org.py.hib.relation.many2many.Teacher"   
				/>  
		</set>  
	</class>  
</hibernate-mapping>
```
**注意**
1. set中的 table 指向的是数据库中的关联表。
1. cascade 用的是save-update , 且inverse用的是false，这样的话，当进行修改和保存和删除时，关联表中的记录也会删掉.
1. 如果cascade 用的是 all 那么连同student表中的记录也会被删除掉。
1. key中的column指的是： 关联表中与Student发生关系的字段。
1. 而many-to-many中的column指的是：关联表中，与class(这里是：org.py.hib.relation.many2many.Teacher)发生关系的字段。

Teacher.hbm.xml
```xml
<?xml version="1.0" encoding="utf-8"?>  
<!DOCTYPE hibernate-mapping PUBLIC "-//Hibernate/Hibernate Mapping DTD 3.0//EN"  
	"http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">  
	
<hibernate-mapping>  
	<class name="org.py.hib.relation.many2many.Teacher"  
		table="teacher">  
		<id name="id" type="java.lang.String" column="tid"  
			length="32">  
			<generator class="uuid" />  
		</id>  
	
		<property name="name" type="java.lang.String" column="name"  
			length="32" not-null="true" />  
	
		<set name="students" table="teacher_student_relation" cascade="save-update"  
			inverse="false">  
			<key column="teacher_id" not-null="true" />  
			<many-to-many class="org.py.hib.relation.many2many.Student"  
				column="student_id" />  
		</set>  
	</class>  
</hibernate-mapping>
```
**注意：** 这里的inverse也采用了false，这样子的话，Teacher和Student都维护关系表中的关系。

测试类，Many2ManyTest.java
```java
import java.util.Iterator;
import java.util.List;
import java.util.Set;

import junit.framework.Assert;
import junit.framework.TestCase;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;
import org.junit.After;
import org.junit.Before;

public class Many2ManyTest extends TestCase {
    private SessionFactory factory;

    @Before
    public void setUp() throws Exception {
        Configuration conf = new Configuration().configure();
        factory = conf.buildSessionFactory();
    }

    public void testSave() throws Exception {
        System.out.println("\n=== test save ===");

        Teacher teacher1 = new Teacher();
        teacher1.setName("teacher_1");

        Teacher teacher2 = new Teacher();
        teacher2.setName("teacher_2");

        Student stu1 = new Student();
        stu1.setName("student_1");

        Student stu2 = new Student();
        stu2.setName("student_2");

        stu1.getTeachers().add(teacher1);
        stu1.getTeachers().add(teacher2);

        stu2.getTeachers().add(teacher2);
        teacher1.getStudents().add(stu2);

        Session session = null;
        Transaction tran = null;
        try {
            session = factory.openSession();
            tran = session.beginTransaction();

            session.save(stu1);
            session.save(stu2);
            tran.commit();

            Assert.assertNotNull(teacher1.getId());
            Assert.assertNotNull(teacher2.getId());

            Assert.assertNotNull(stu1.getId());
            Assert.assertNotNull(stu2.getId());

        } catch (Exception ex) {
            tran.rollback();
            throw ex;
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (Exception ex) {
                    // nothing to do
                } finally {
                    if (session != null)
                        session = null;
                }
            }
        }
    }

    @SuppressWarnings("unchecked")
    public void testFindFromTeacher() throws Exception {
        System.out.println("\n=== test find from Teacher ===");
        Session session = null;
        try {
            session = factory.openSession();
            Iterator iter = session.createQuery("from Teacher").iterate();
            while (iter.hasNext()) {
                Teacher teacher = iter.next();
                Assert.assertNotNull(teacher.getId());
                String teacherName = teacher.getName();
                if ("teacher_1".equals(teacherName)) {
                    Set stus = teacher.getStudents();
                    Assert.assertEquals(stus.size(), 2);
                    for (Student stu : stus) {
                        String stuName = stu.getName();
                        Assert.assertNotNull(stu.getId());
                        Assert.assertTrue(stuName.equals("student_1") || stuName.equals("student_2"));
                    }
                } else if ("teacher_2".equals(teacherName)) {
                    Set stus = teacher.getStudents();
                    Assert.assertEquals(stus.size(), 2);

                    for (Student stu : stus) {
                        String stuName = stu.getName();
                        Assert.assertNotNull(stu.getId());
                        Assert.assertTrue(stuName.equals("student_1") || stuName.equals("student_2"));
                    }
                } else {
                    throw new Exception("teacher name error exception.");
                }
            }
        } catch (Exception ex) {
            throw ex;
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (Exception ex) {
                    // nothing to do
                } finally {
                    if (session != null)
                        session = null;
                }
            }
        }
    }

    @SuppressWarnings("unchecked")
    public void testFindFromStudent() throws Exception {
        System.out.println("\n=== test find from Student ===");
        Session session = null;
        try {
            session = factory.openSession();
            Iterator iter = session.createQuery("from Student").iterate();
            while (iter.hasNext()) {
                Student stu = iter.next();
                Assert.assertNotNull(stu.getId());
                String stuName = stu.getName();
                if ("student_1".equals(stuName)) {
                    Set teachers = stu.getTeachers();
                    Assert.assertEquals(teachers.size(), 2);
                    for (Teacher teacher : teachers) {
                        String tName = teacher.getName();
                        Assert.assertNotNull(teacher.getId());
                        Assert.assertTrue(tName.equals("teacher_1") || tName.equals("teacher_2"));
                    }
                } else if ("student_2".equals(stuName)) {
                    Set teachers = stu.getTeachers();
                    Assert.assertEquals(teachers.size(), 2);
                    for (Teacher teacher : teachers) {
                        String tName = teacher.getName();
                        Assert.assertNotNull(teacher.getId());
                        Assert.assertTrue(tName.equals("teacher_1") || tName.equals("teacher_2"));
                    }
                } else {
                    throw new Exception("student name error exception.");
                }
            }
        } catch (Exception ex) {
            throw ex;
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (Exception ex) {
                    // nothing to do
                } finally {
                    if (session != null)
                        session = null;
                }
            }
        }
    }

    public void testModify() throws Exception {
        System.out.println("\n=== test modify ===");
        Session session = null;
        Transaction tran = null;
        try {
            session = factory.openSession();
            tran = session.beginTransaction();

            Teacher t1 = (Teacher) session.createQuery("from Teacher t where t.name='teacher_1'").list().get(0);
            t1.setName("new_teacher_1"); // 修改用户名 = m_name2.（原来用户名= m_name）

            Set stus = t1.getStudents();
            for (Student stu : stus) {
                if (stu.getName().equals("student_1")) {
                    stus.remove(stu);
                    break;
                }
            }

            tran.commit();

        } catch (Exception ex) {
            throw ex;
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (Exception ex) {
                    // nothing to do
                } finally {
                    if (session != null)
                        session = null;
                }
            }
        }

        /*
         * 修改后再查询
         */
        System.out.println("\n=== test find from Teacher after modify===");
        try {
            session = factory.openSession();
            Iterator iter = session.createQuery("from Teacher").iterate();
            while (iter.hasNext()) {
                Teacher teacher = iter.next();
                Assert.assertNotNull(teacher.getId());
                String teacherName = teacher.getName();
                if ("new_teacher_1".equals(teacherName)) {
                    Set stus = teacher.getStudents();
                    Assert.assertEquals(stus.size(), 1);
                    for (Student stu : stus) {
                        String stuName = stu.getName();
                        Assert.assertNotNull(stu.getId());
                        Assert.assertTrue(stuName.equals("student_2"));
                    }
                } else if ("teacher_2".equals(teacherName)) {
                    Set stus = teacher.getStudents();
                    Assert.assertEquals(stus.size(), 2);

                    for (Student stu : stus) {
                        String stuName = stu.getName();
                        Assert.assertNotNull(stu.getId());
                        Assert.assertTrue(stuName.equals("student_1") || stuName.equals("student_2"));
                    }
                } else {
                    throw new Exception("teacher name error exception.");
                }
            }
        } catch (Exception ex) {
            throw ex;
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (Exception ex) {
                    // nothing to do
                } finally {
                    if (session != null)
                        session = null;
                }
            }
        }
    }

    public void testDelete() throws Exception {
        System.out.println("\n=== test delete ===");
        Session session = null;
        Transaction tran = null;
        try {
            session = factory.openSession();
            tran = session.beginTransaction();

            Iterator iter = session.createQuery("from Teacher").iterate();
            while (iter.hasNext())
                session.delete(iter.next());

            tran.commit();

            Integer count = (Integer) session.createQuery("select count(*) from Teacher").list().get(0);
            Assert.assertEquals(0, count.intValue());

        } catch (Exception ex) {
            throw ex;
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (Exception ex) {
                    // nothing to do
                } finally {
                    if (session != null)
                        session = null;
                }
            }
        }

        /*
         * 删除后再查询
         */
        System.out.println("\n=== test find after delete ===");
        try {
            session = factory.openSession();

            Integer num = (Integer) session.createQuery("from Teacher").list().size();
            Assert.assertEquals(0, num.intValue());

            num = (Integer) session.createQuery("from Student").list().size();
            Assert.assertEquals(0, num.intValue());

        } catch (Exception ex) {
            throw ex;
        } finally {
            if (session != null) {
                try {
                    session.close();
                } catch (Exception ex) {
                    // nothing to do
                } finally {
                    if (session != null)
                        session = null;
                }
            }
        }
    }

    @After
    public void tearDown() throws Exception {
        factory.close();
    }

}
```
从这个例子中可以看出，many-to-many中，需要引入第3张表来表示关系。

## xml关系映射 - 复杂的case

需求：丈夫有1个妻子，这样是1夫1妻。但是，丈夫花心，同时有多个情妇。

例子归例子，大家不要做这样的丈夫。只是为了更加深入记忆。

### DB
先看sql：

```sql
use HibernateQuickUse;

drop table if exists Paramour;
drop table if exists Husband;
drop table if exists Wife;

create table Wife (
	wid varchar(32) primary key,
	name varchar(128) not null
);


create table Husband (
	hid varchar(32) primary key,
	name varchar(32) not null,
	wife_id varchar(32) not null,
	foreign key(wife_id) references Wife(wid)
);

create table Paramour (
	pid varchar(32)  primary key,
	name varchar(128) not null,
	husband_id varchar(32) not null,
	foreign key(husband_id) references Husband(hid)
);
```

### Pojo
然后看java文件。

Husband.java
```java
import java.util.HashSet;
import java.util.Set;

@SuppressWarnings("serial")
public class Husband implements java.io.Serializable {
	private String id;
	private String name;
	private Wife wife;
	private Set paramours = new HashSet();

	public Husband(){}

	public String getId() { return id;}
	public void setId(String id) { this.id = id;}

	public String getName() { return name;}
	public void setName(String name) { this.name = name;}

	public Wife getWife() { return wife;}
	public void setWife(Wife wife) { this.wife = wife;}

	public Set getParamours() { return paramours;}
	public void setParamours(Set paramours) { this.paramours = paramours;}
}
```

Wife.java

```java
@SuppressWarnings("serial")
public class Wife implements java.io.Serializable {
	private String id;
	private String name;

	public Wife() { }

	public String getId() { return id; }
	public void setId(String id) { this.id = id; }

	public String getName() { return this.name; }
	public void setName(String name) { this.name = name; }
}
```

Paramour.java
```java
@SuppressWarnings("serial")
public class Paramour implements java.io.Serializable {
	private String id;
	private String name;
	private Husband husband;

	public Paramour(){ }

	public String getId() { return id; }
	public void setId(String id) { this.id = id; }

	public Husband getHusband() { return this.husband; }
	public void setHusband(Husband husband) { this.husband = husband; }

	public String getName() { return this.name; }
	public void setName(String name) { this.name = name; }
}
```

### Mapping Xml
接下来再看xml映射文件。

Husband.hbm.xml
```xml
<?xml version="1.0" encoding="utf-8"?>  
<!DOCTYPE hibernate-mapping PUBLIC "-//Hibernate/Hibernate Mapping DTD 3.0//EN"  
	"http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">  
	
<hibernate-mapping>  
	<class name="org.py.hib.relation.complex.Husband" table="husband">  
		<id name="id" type="java.lang.String" column="hid"  
			length="32">  
			<generator class="uuid" />  
		</id>  
	
		<property name="name" type="java.lang.String" column="name"  
			length="32" not-null="true" />  
	
		<many-to-one name="wife" class="org.py.hib.relation.complex.Wife" cascade="all" column="wife_id" />  
				
		<set name="paramours" cascade="all" inverse="true" >  
			<key column="husband_id" />  
			<one-to-many class="org.py.hib.relation.complex.Paramour" />  
		</set>  
	</class>  
</hibernate-mapping> 
```

Wife.hbm.xml
```xml
<?xml version="1.0" encoding="utf-8"?>  
<!DOCTYPE hibernate-mapping PUBLIC "-//Hibernate/Hibernate Mapping DTD 3.0//EN"  
	"http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">  
	
<hibernate-mapping>  
	<class name="org.py.hib.relation.complex.Wife" table="wife">  
		<id name="id" type="java.lang.String" column="wid" length="32">  
			<generator class="uuid" />  
		</id>  
	
		<property name="name" type="java.lang.String" column="name"  length="128" not-null="true" />  
	
	</class>  
</hibernate-mapping> 
```

Paramour.hbm.xml
```xml
<?xml version="1.0" encoding="utf-8"?>  
<!DOCTYPE hibernate-mapping PUBLIC "-//Hibernate/Hibernate Mapping DTD 3.0//EN"  
	"http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">   
<hibernate-mapping>  
	<class name="org.py.hib.relation.complex.Paramour" table="paramour">  
		<id name="id" type="java.lang.String" column="pid">  
			<generator class="uuid" />  
		</id>  
	
		<property name="name" type="java.lang.String" column="name" not-null="true" />  
	
		<many-to-one name="husband" class="org.py.hib.relation.complex.Husband" column="husband_id" />  
			
	</class>  
		
</hibernate-mapping> 
```

### Testing
这里只测试了save。其他的测试大家感兴趣的可以补充。
ComplexTest.java
```java
import junit.framework.Assert;
import junit.framework.TestCase;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;
import org.junit.After;
import org.junit.Before;

/**
 * 这个测试忽略了hibernate的异常
 **/
public class ComplexTest extends TestCase {
	private SessionFactory factory;

	@Before
	public void setUp() throws Exception {
		Configuration conf = new Configuration().configure();
		factory = conf.buildSessionFactory();
	}

	public void testSave() {
		Session session = factory.openSession();
		Transaction tran = session.beginTransaction();

		Husband hus = new Husband();
		hus.setName("husband");

		Wife wife = new Wife();
		wife.setName("wife");

		Paramour p1 = new Paramour();
		p1.setName("paramour_1");

		Paramour p2 = new Paramour();
		p2.setName("paramour_2");

		Paramour p3 = new Paramour();
		p3.setName("paramour_3");

		hus.setWife(wife);

		hus.getParamours().add(p1);
		hus.getParamours().add(p2);
		hus.getParamours().add(p3);

		p1.setHusband(hus);
		p2.setHusband(hus);
		p3.setHusband(hus);
		
		session.save(hus);

		tran.commit();

		Assert.assertNotNull(hus.getId());
		Assert.assertNotNull(wife.getId());

		Assert.assertNotNull(p1.getId());
		Assert.assertNotNull(p2.getId());
		Assert.assertNotNull(p3.getId());
		
		session.close();
	}

	@After
	public void tearDown() {
		factory.close();
	}
}
```

## annotation关系映射 1:1
讲完了xml的关系映射，下面讲一下annatation的关系映射
这讲OneToOne的用法。而且是基于主外键的关联。因为这个是实际开发中最最常见的。

这里先说明一下，我的java类的命名都以Test开头。而对应的对象名却没有用test开头。这里是为了更好的说明注视中的value到底是类名还是对象名。

### Pojo
先看java代码：

TestUser.java
```java
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.OneToOne;

@Entity
public class TestUser
{
	String   id;
	String   username;
	TestCard card;

	@Id
	public String getId() {return id; }
	public void setId(String id) {this.id = id; }

	public String getUsername() {return username; }
	public void setUsername(String username) {this.username = username; }

	@OneToOne
	public TestCard getCard() {return card; }
	public void setCard(TestCard card) {this.card = card; }
}
```

TestCard：
```java
import javax.persistence.Entity;
import javax.persistence.Id;

@Entity
public class TestCard
{
	String id;
	String cardNumber;

	@Id
	public String getId() { return id; }
	public void setId(String id) { this.id = id; }

	public String getCardNumber() { return cardNumber; }
	public void setCardNumber(String cardNumber) { this.cardNumber = cardNumber; }
}
```
这样子就是OneToOne了。这个是单向的关系，即：由TestCard控制TestUser。看sql语句就知道了。

### DB
hibernate自动生成的sql为：
```sql
drop table test_card cascade constraints;

drop table test_user cascade constraints;

create table test_card (
	id varchar2(255 char) not null,
	card_number varchar2(255 char),
	primary key (id)
);

create table test_user (
	id varchar2(255 char) not null,
	username varchar2(255 char),
	card_id varchar2(255 char),
	primary key (id)
);

alter table test_user add constraint FKB9A96B58A237D846 foreign key (card_id) references test_card;
```
个人认为，应该这样子理解OneToOne。

1. 首先，他是用来声明在方法上的。（这句好似废话）
1. 然后，他其实是用来annation这个方法的返回值的。即：描述TestCard的。
    > 也就是说：TestCard 为控制方。TestUser为被控方。那么对应的表中，test_user表有一个外键字段对应着test_card表中的一个主键。

这样，就好理解了。

上面的为单向关联。那么，双向关联呢？修改TestCard如下：
```java
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.OneToOne;

@Entity
public class TestCard {
	String   id;
	String   cardNumber;
	TestUser user;

	@Id
	public String getId() { return id; }
	public void setId(String id) { this.id = id; }

	@OneToOne
	public TestUser getUser() { return user; }
	public void setUser(TestUser user) { this.user = user; }

	
	public String getCardNumber() { return cardNumber; }
	public void setCardNumber(String cardNumber) { this.cardNumber = cardNumber; }
}
```

这样，产生的sql为：
```sql
drop table test_card cascade constraints;
drop table test_user cascade constraints;

create table test_card (
	id varchar2(255 char) not null,
	card_number varchar2(255 char),
	user_id varchar2(255 char),
	primary key (id)
);

create table test_user (
	id varchar2(255 char) not null,
	username varchar2(255 char),
	card_id varchar2(255 char),
	primary key (id)
);

alter table test_card add constraint FKB9A0FA9D7876DA66 foreign key (user_id) references test_user;

alter table test_user add constraint FKB9A96B58A237D846 foreign key (card_id) references test_card;
```

可以看到，当我双方都声明了OneToOne时候，也就达到了双向的One2One效果。但是很遗憾。Hibernate不知道你由哪边控制哪边，或者说由哪边来维护关系。所以，他生成的sql语句中可以看到，都有test_card和test_user是相互关联的，即：都有FK关联上堆放的PK。很明显，这个不是我们要的效果。

我们需要的是，pojo中能双向one2one，但是db中不需要。所以，我们需要修改一下。


修改TestCard.java代码：
```java
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.OneToOne;

@Entity
public class TestCard {
	String   id;
	String   cardNumber;
	TestUser user;

	@Id
	public String getId() { return id; }
	public void setId(String id) { this.id = id; }

	@OneToOne(mappedBy="card")
	public TestUser getUser() { return user; }
	public void setUser(TestUser user) { this.user = user; }

	public String getCardNumber() { return cardNumber; }
	public void setCardNumber(String cardNumber) { this.cardNumber = cardNumber; }
}
```
**注意：** OneToOne中的mappedBy就指出了此处返回的TestUser对应的test_user表中有一个指向TestUser的属性"card"的外键。可以看sql。
```sql
drop table test_card cascade constraints;

drop table test_user cascade constraints;

create table test_card (
	id varchar2(255 char) not null,
	card_number varchar2(255 char),
	primary key (id)
);

create table test_user (
	id varchar2(255 char) not null,
	username varchar2(255 char),
	card_id varchar2(255 char),
	primary key (id)
);

alter table test_user add constraint FKB9A96B58A237D846 foreign key (card_id) references test_card;
```
而这得"mappedBy=card"中的card是TestUser中的TestCard类型的成员变量名。这也就是为什么我要用Test修饰类名，而对象名却不用的理由。

或者，还可以这样子来理解OneToOne。

1.单向OneToOne中。声明了OneToOne这个Annotation的方法，他的返回值即：维护方。(主键方)
1.双向OneToOne中。在OneToOne中声明了mappedBy="xx"的，他的返回值即：被维护方。(外键方)

## annotation的关系映射 1:n
这次说说OneToMany和ManyToOne

我们的场景是 1个父亲n多个孩子

### Pojo
先来看看这中做法：

TestFather.java
```java
import java.util.ArrayList;
import java.util.List;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.OneToMany;

@Entity
public class TestFather{
	String          id;
	String          name;
	List children = new ArrayList();

	@Id
	public String getId() { return id; }
	public void setId(String id) { this.id = id; }

	public String getName() { return name; }
	public void setName(String name) { this.name = name; }

	@OneToMany
	public List getChildren() { return children; }
	public void setChildren(List children) { this.children = children; }
}
```

TestChild.java
```Java
import javax.persistence.Entity;
import javax.persistence.Id;

@Entity
public class TestChild {
	String     id;
	String     name;

	@Id
	public String getId() { return id; }
	public void setId(String id) { this.id = id; }

	public String getName() { return name; }
	public void setName(String name) { this.name = name; }
}
```

### DB
这样子，好像就可以了。那么是的么？我们来看看hib产生的sql

``` sql
drop table test_child cascade constraints;
drop table test_father cascade constraints;
drop table test_father_children cascade constraints;

create table test_child (
	id varchar2(255 char) not null,
	name varchar2(255 char),
	primary key (id)
);

create table test_father (
	id varchar2(255 char) not null,
	name varchar2(255 char),
	primary key (id)
);

create table test_father_children (
	null_id varchar2(255 char) not null,
	children_id varchar2(255 char) not null,
	unique (children_id)
);

alter table test_father_children 
	add constraint FK2E6E87D5901B7DBB 
	foreign key (null_id) 
	references test_father;

alter table test_father_children 
	add constraint FK2E6E87D58CD0E56B 
	foreign key (children_id) 
	references test_child;

alter table test_user 
	add constraint FKB9A96B58A237D846 
	foreign key (card_id) 
	references test_card;
```
oh！ My God ！它居然又帮我们多创建了一个table。作为关联。太笨了。

很明显，这不是我们所需要的。

那我们该如何呢？这就需要ManyToMany了。

## annotation的关系映射 n:n
场景：Product和Customer。

### Pojo
先看TestProduct.java
```java    
import java.util.ArrayList;
import java.util.List;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.ManyToMany;

@Entity
public class TestProduct
{
	private String             id;
	private String             name;
	private float              price;
	private List customers = new ArrayList();

	@Id
	public String getId() { return id; }
	public void setId(String id) { this.id = id; }

	public String getName() { return name; }
	public void setName(String name) { this.name = name; }

	public float getPrice() { return price; }
	public void setPrice(float price) { this.price = price; }

	@ManyToMany
	public List getCustomers() { return customers; }
	public void setCustomers(List customers) { this.customers = customers; }

}
```

注意这里的ManyToMany什么都没有写。

再看TestCustomer.java
```java
import java.util.ArrayList;
import java.util.List;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.ManyToMany;

@Entity
public class TestCustomer {
	private String            id;
	private String            tel;
	private List products = new ArrayList();

	@Id
	public String getId() { return id; }
	public void setId(String id) { this.id = id; }

	public String getTel() { return tel; }
	public void setTel(String tel) { this.tel = tel; }

	@ManyToMany(mappedBy = "customers")
	public List getProducts() { return products; }
	public void setProducts(List products) { this.products = products; }
}
```
**注意：**这里的ManyToMany我写了mappedBy这个attribute。

### DB
然后看hib产生的sql:
```sql
drop table test_customer cascade constraints;
drop table test_product cascade constraints;
drop table test_product_customers cascade constraints;

create table test_customer (
	id varchar2(255 char) not null,
	tel varchar2(255 char),
	primary key (id)
);

create table test_product (
	id varchar2(255 char) not null,
	price float not null,
	name varchar2(255 char),
	primary key (id)
);

create table test_product_customers (
	products_id varchar2(255 char) not null,
	customers_id varchar2(255 char) not null
);
```

ok! 非常好。hib终于在ManyToMany上没有犯白痴了。

上面强调了mappedBy这个属性。其实，之前有提到mappedBy这个东西。只是，我没有说到底是什么意思。其实很简单：这个东西就相当于xml配置中的inverse。写了mappedBy就代表这个方法的返回值是被维护方。
