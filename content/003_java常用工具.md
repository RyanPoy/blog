+++
title = "java常用工具"
date = 2008-10-17

[taxonomies]
categories = ["Tech"]
tags = ["Java"]
+++

在进行网络编程的时候，进行走的是2进制协议。

一般一个package定义为4个字节的len，和len个字节的长度。

这个时候，一个对字节进行操作，功能类似于StringBuffer的工具，就显得尤为重要了。

所以，对其进行了封装。

    import java.io.*;
    import java.util.zip.GZIPInputStream;
    
    public class ByteBuffer
    {
    	byte[] bytes;
    
    	int used;
    
    	public ByteBuffer()
    	{
    		bytes = new byte[1024];
    		used = 0;
    	}
    
    	public ByteBuffer(int size)
    	{
    		bytes = new byte[size];
    		used = 0;
    	}
    
    	public int getUsed()
    	{
    		return used;
    	}
    
    	public ByteBuffer append(byte b)
    	{
    		if (used + 1 >= bytes.length)
    		{
    			byte[] bb = new byte[bytes.length << 1];
    			copy(bb, 0, bytes, 0, used);
    			bytes = bb;
    		}
    		bytes[used] = b;
    		used++;
    		return this;
    	}
    
    	public ByteBuffer append(byte[] b)
    	{
    		return append(b, 0, b.length);
    	}
    
    	public ByteBuffer append(byte[] b, int begin, int len)
    	{
    		if (b == null)
    			return this;
    		if (bytes.length < used + len)
    		{
    			byte[] bb = new byte[(used + len) << 1];
    			copy(bb, 0, bytes, 0, used);
    			bytes = bb;
    		}
    		copy(bytes, used, b, begin, len);
    		used += len;
    		return this;
    	}
    
    	public ByteBuffer append(short v)
    	{
    		byte[] b = new byte[2];
    		for (int i = 0; i < 2; i++)
    			b[i] = (byte) ((v >> (i * 8)) & 0x00ff);
    		return append(b, 0, 2);
    	}
    
    	public ByteBuffer append(int v)
    	{
    		byte[] b = new byte[4];
    		for (int i = 0; i < 4; i++)
    			b[i] = (byte) ((v >> (i * 8)) & 0x00ff);
    		return append(b, 0, 4);
    	}
    
    	public ByteBuffer append(long v)
    	{
    		byte[] b = new byte[8];
    		for (int i = 0; i < 8; i++)
    			b[i] = (byte) ((v >> (i * 8)) & 0x00ff);
    		return append(b, 0, 8);
    	}
    
    	public ByteBuffer append(boolean v)
    	{
    		if (true == v)
    			return append((byte) 1);
    		else
    			return append((byte) 0);
    	}
    
    	public ByteBuffer append(String str, String charset)
    	{
    		byte[] b;
    		try
    		{
    			b = str.getBytes(charset);
    		} catch (UnsupportedEncodingException e)
    		{
    			throw new RuntimeException(charset + "error !");
    		}
    		return append(b, 0, b.length);
    	}
    
    	public ByteBuffer append(String str)
    	{
    		byte[] b = str.getBytes();
    		return append(b, 0, b.length);
    	}
    
    	public ByteBuffer append(ByteBuffer bb)
    	{
    		return append(bb.array(), 0, bb.used);
    	}
    
    	private final void copy(byte[] dest, int destStart, byte[] src, int srcBegin, int len)
    	{
    		for (int i = 0; i < len; i++)
    			dest[destStart + i] = src[srcBegin + i];
    	}
    
    	public byte[] array()
    	{
    		return bytes;
    	}
    
    	public String toString(String encoding) throws UnsupportedEncodingException
    	{
    		return new String(bytes, 0, used, encoding);
    	}
    
    	public String toString()
    	{
    		return new String(bytes, 0, used);
    	}
    
    	public String toString(int size, String encoding) throws UnsupportedEncodingException
    	{
    		return new String(bytes, 0, (used > size) ? size : used, encoding);
    	}
    
    	/**
    	 * ungzip
    	 */
    	public void ungzip() throws IOException
    	{
    		ByteArrayInputStream bIn = new ByteArrayInputStream(bytes);
    		GZIPInputStream gIn = new GZIPInputStream(bIn);
    		ByteBuffer bb = new ByteBuffer(bytes.length * 2);
    		byte[] bs = new byte[1024];
    		int len = 0;
    		while ((len = gIn.read(bs, 0, 1024)) > 0)
    			bb.append(bs, 0, len);
    		bytes = bb.bytes;
    	}
    
    	public void clear()
    	{
    		this.used = 0;
    	}
    
    	public static void main(String[] argv) throws IOException
    	{
    
    		byte[] b = new byte[1024];
    		for (int i = 0; i < 3; i++)
    			b[i] = 'c';
    		ByteBuffer bb = new ByteBuffer(4);
    		bb.append(b, 0, 3).append(b, 0, 3);
    		System.out.print(bb.toString());
    
    		ByteBuffer buffer = new ByteBuffer(1);
    		buffer.append((byte) 1);
    		buffer.append((byte) 2);
    		buffer.append((byte) 3);
    		buffer.append((byte) 4);
    		buffer.append((byte) 5);
    		buffer.append((byte) 6);
    		buffer.append(10);
    		buffer.append(10L);
    		buffer.append((short) 10);
    		buffer.append("abcdefg");
    		buffer.append("OPQRSTV", "gb2312");
    		buffer.array();
    
    	}
    }
java原生提供了一些数据类型的转换，比方说：string -> int, int -> string, float -> string,  string -> float 等等。但是，对于blog -> string，string -> blog, clob -> string, string -> clob 没有, 为了方便的解决各个类型中的相互转化，特地封装了这个工具

    import java.io.BufferedReader;
    import java.io.IOException;
    import java.io.InputStreamReader;
    import java.sql.Blob;
    import java.sql.Clob;
    
    public class Convert
    {
    	/**
    	 * convert a string to a byte
    	 * @param s
    	 * @return byte
    	 */
    	public static byte str2Byte(String s)
    	{
    		if (s == null || s.trim().length() == 0)
    			return 0;
    		return Byte.parseByte(s);
    	}
    
    	/**
    	 * convert a string to a short
    	 * @param s
    	 * @return short
    	 */
    	public static short str2Short(String s)
    	{
    		if (s == null || s.trim().length() == 0)
    			return 0;
    		return Short.parseShort(s);
    	}
    
    	/**
    	 * convert a string to a int
    	 * @param s
    	 * @return
    	 */
    	public static int str2Int(String s)
    	{
    		if (s == null || s.trim().length() == 0)
    			return 0;
    		return Integer.parseInt(s);
    	}
    
    	/**
    	 * convert a string to a long
    	 * @param s
    	 * @return
    	 */
    	public static long str2Long(String s)
    	{
    		if (s == null || s.trim().length() == 0)
    			return 0;
    		return Long.parseLong(s);
    	}
    
    	/**
    	 * convert a string a float
    	 * @param s
    	 * @return
    	 */
    	public static float str2Float(String s)
    	{
    		if (s == null || s.trim().length() == 0)
    			return 0.0F;
    		return Float.parseFloat(s);
    	}
    
    	/**
    	 * convert a string to a double
    	 * @param s
    	 * @return
    	 */
    	public static double str2Double(String s)
    	{
    		if (s == null || s.trim().length() == 0)
    			return 0;
    		return Double.parseDouble(s);
    	}
    
    	/**
    	 * convert a string to a boolean
    	 * @param s
    	 * @return
    	 */
    	public static boolean str2Bool(String s)
    	{
    		if (s == null || s.trim().length() == 0)
    			return false;
    		else if (s.trim().equalsIgnoreCase("true"))
    			return true;
    		else if (s.trim().equals("1"))
    			return true;
    		else
    			return false;
    	}
    
    	/**
    	 * convert a string to a byte array
    	 * @param str
    	 * @param charset
    	 * @return
    	 * @throws IOException
    	 * @throws Exception
    	 */
    	public static byte[] str2Bytes(String str, String charset) throws IOException
    	{
    		if (null == charset)
    			return str.getBytes();
    		return str.getBytes(charset);
    	}
    
    	/**
    	 * join two byte arrays to one byte array
    	 * @param fir
    	 * @param sec
    	 * @return
    	 */
    	public static byte[] joinBytes(byte[] fir, byte[] sec)
    	{
    		int firLen = fir.length;
    		int secLen = sec.length;
    		byte[] third = new byte[firLen + secLen];
    
    		for (int i = 0; i < firLen; i++)
    			third[i] = fir[i];
    		for (int i = 0; i < secLen; i++)
    			third[firLen + i] = sec[i];
    
    		return third;
    	}
    
    	/**
    	 * convert a long value to bytes array
    	 * @param num
    	 * @return
    	 */
    	public static byte[] long2Bytes(long num)
    	{
    		byte[] b = new byte[8];
    		for (int i = 0; i < b.length; i++)
    			b[i] = (byte) ((num >> (i * 8)) & 0xff);
    		return b;
    	}
    
    	/**
    	 * convert a long value to a boolean value
    	 * @param num
    	 * @return
    	 */
    	public static boolean long2Bool(long num)
    	{
    		if (num == 0)
    			return false;
    		return true;
    	}
    
    	/**
    	 * convert a byte array to a long
    	 * @param b
    	 * @return
    	 */
    	public static long bytes2Long(byte[] b)
    	{
    		return bytes2Long(b, 0);
    	}
    
    	/**
    	 * convert a byte array to a long
    	 * @param b
    	 * @param start
    	 * @return
    	 */
    	public static long bytes2Long(byte[] b, int start)
    	{
    		long result = 0;
    		for (int i = 0; i < 8; i++)
    			result += (long) (((long) (b[start + i]) & 0xff) << (i * 8));
    		return result;
    	}
    
    	/**
    	 * convert a int to a byte array
    	 * @param num
    	 * @return
    	 */
    	public static byte[] int2Bytes(int num)
    	{
    		byte[] b = new byte[4];
    		for (int i = 0; i < b.length; i++)
    			b[i] = (byte) ((num >> (i * 8)) & 0xff);
    		return b;
    	}
    
    	/**
    	 * convert a int to a boolean value
    	 * @param num
    	 * @return
    	 */
    	public static boolean int2Bool(int num)
    	{
    		if (num == 0)
    			return false;
    		return true;
    	}
    
    	/**
    	 * convert a byte array to a int
    	 * @param b
    	 * @return
    	 */
    	public static int bytes2Int(byte[] b)
    	{
    		return bytes2Int(b, 0);
    	}
    
    	/**
    	 * convert a byte array to a int
    	 * @param b
    	 * @param start
    	 * @return
    	 */
    	public static int bytes2Int(byte[] b, int start)
    	{
    		int result = 0;
    		for (int i = 0; i < 4; i++)
    			result += (long) (((int) (b[start + i]) & 0xff) << (i * 8));
    		return result;
    	}
    
    	/**
    	 * convert a blob data to a string
    	 * @param blob
    	 * @return
    	 * @throws Exception
    	 */
    	public static String blob2Str(Blob blob) throws Exception
    	{
    		if (blob == null)
    			return "";
    		StringBuffer buffer = new StringBuffer(1024);
    		BufferedReader in = null;
    		try
    		{
    			String str = null;
    			in = new BufferedReader(new InputStreamReader(blob.getBinaryStream()));
    			while ((str = in.readLine()) != null)
    				buffer.append(str).append("\r\n");
    		} catch (Exception e)
    		{
    			throw e;
    		} finally
    		{
    			try
    			{
    				in.close();
    			} catch (Exception e)
    			{
    				if (null != in)
    					in = null;
    			}
    		}
    
    		return buffer.toString();
    	}
    
    	/**
    	 * convert a clob data to a string
    	 * @param clob
    	 * @return
    	 * @throws Exception
    	 */
    	public static String clob2Str(Clob clob) throws Exception
    	{
    		if (clob == null)
    			return "";
    		StringBuffer buffer = new StringBuffer(1024);
    		BufferedReader in = null;
    		try
    		{
    			String str = null;
    			in = new BufferedReader(clob.getCharacterStream());
    			while ((str = in.readLine()) != null)
    				buffer.append(str).append("\r\n");
    
    		} catch (Exception ex)
    		{
    			throw ex;
    		} finally
    		{
    			try
    			{
    				in.close();
    			} catch (Exception e)
    			{
    				in = null;
    			}
    		}
    		return buffer.toString();
    	}
    
    	public static boolean byte2Bool(byte v)
    	{
    		if (v == (byte) 0)
    			return false;
    		else
    			return true;
    	}
    
    	public static byte bool2Byte(boolean b)
    	{
    		if (b == false)
    			return (byte) 0;
    		else
    			return (byte) 1;
    	}
    
    	public static String str2Filepath(String str)
    	{
    		if (str == null || str.trim().length() == 0)
    			return str;
    		String separator = System.getProperty("file.separator");
    		if (!str.endsWith("\\") && !str.endsWith("/"))
    			str += separator;
    		return str;
    	}
    
    	public static String str2Webpath(String str)
    	{
    		if (str == null || str.trim().length() == 0)
    			return str;
    		if (!str.endsWith("/"))
    			str += "/";
    		return str;
    	}
    
    }
java的Date不推荐使用了，而推荐使用Calender，但是Calender确实难用。经常要转几个弯，才能得到自己需要的结果，所以，封装了这个东西，方便以后使用。

代码中的Convert请看：[java常用工具-Convert][1]

    import java.text.ParseException;
    import java.text.SimpleDateFormat;
    import java.util.Calendar;
    import java.util.Date;
    
    import Convert;
    
    public class DateUtil
    {
    	/**
    	 * convert a date string to a Date data with the format default format: yyyy-MM-dd
    	 * @param datestr
    	 * @param format
    	 * @return
    	 * @throws ParseException
    	 */
    	public static Date str2Date(String datestr, String format) throws ParseException
    	{
    		if (datestr == null)
    			return null;
    		if (format == null)
    			format = "yyyy-MM-dd";
    		SimpleDateFormat sdf = new SimpleDateFormat(format);
    		return sdf.parse(datestr);
    	}
    
    	public static String long2Datestr(long time, String format)
    	{
    		if (format == null || format.trim().equals(""))
    			format = "yyyy-MM-dd HH:mm:ss";
    
    		SimpleDateFormat sdf = new SimpleDateFormat(format);
    		return sdf.format(time);
    	}
    
    	/**
    	 * convert a date to a format string default format:yyyy-MM-dd HH:mm:ss
    	 * @param date
    	 * @param format
    	 * @return
    	 */
    	public static String date2Str(Date date, String format)
    	{
    		if (date != null)
    			return long2Datestr(date.getTime(), format);
    		else
    			return long2Datestr(new Date().getTime(), format);
    	}
    
    	/**
    	 * 得到当天指定时分秒的毫秒数
    	 * @param hour int
    	 * @param min int
    	 * @return long
    	 */
    	public static long getTimeWithHourAndMin(int hour, int min)
    	{
    		Calendar cal = Calendar.getInstance();
    		int year = cal.get(Calendar.YEAR);
    		int month = cal.get(Calendar.MONTH);
    		int day = cal.get(Calendar.DAY_OF_MONTH);
    		cal.set(year, month, day, hour, min);
    		return cal.getTimeInMillis();
    	}
    
    	/**
    	 * 得到当天指定时分秒的毫秒数
    	 * @param HHMin String 为格式串 HH:min
    	 * @return long
    	 */
    	public static long getTimeWithHourAndMin(String HHMin)
    	{
    		HHMin = HHMin.trim();
    		int h = Convert.str2Int(HHMin.substring(0, HHMin.indexOf(":")));
    		int m = Convert.str2Int(HHMin.substring(HHMin.indexOf(":") + 1, HHMin.length()));
    		return getTimeWithHourAndMin(h, m);
    	}
    
    	public static long getYear(Date date)
    	{
    		Calendar cal = Calendar.getInstance();
    		cal.setTime(date);
    		return cal.get(Calendar.YEAR);
    	}
    
    	public static long getMonth(Date date)
    	{
    		Calendar cal = Calendar.getInstance();
    		cal.setTime(date);
    		return cal.get(Calendar.MONTH) + 1;
    	}
    
    	public static void main(String[] args) throws ParseException
    	{
    
    		long time = 1326956252000L;
    		Date d = new Date();
    		d.setTime(time);
    		System.out.println(DateUtil.long2Datestr(time, null));
    		System.out.println(DateUtil.date2Str(d, null));
    		System.out.println("==============================");
    		System.out.println(DateUtil.str2Date("2007-11-19 14:14:59", "yyyy-MM-dd HH:mm:ss").getTime());
    	}
    }


  [1]: /blogs/13
经常需要对项目进行配置。而项目可能是b/s 和 c/s。所以，一个统一的配置读取很重要。
我的习惯。

 - 对于c/s: 直接存放到当前的conf目录下面 
 - 对于b/s: 存放到WEB-INF/conf目录下面

所以，为了方便，封装了如下的工具。

    import java.io.File;
    import java.io.FileOutputStream;
    import java.io.InputStream;
    import java.util.Properties;
    
    public class SysConf
    {
    	private static String confPath;
    
    	private static String sysPath;
    
    	private static String webPath;
    
    	private String filename;
    
    	public SysConf(String filename)
    	{
    		this.filename = filename;
    	}
    
    	public SysConf()
    	{
    	}
    
    	public Properties read(String filename) throws Exception
    	{
    		this.filename = filename;
    		return read();
    	}
    
    	public Properties read() throws Exception
    	{
    		String path = getConfPath();
    		Properties props = new Properties();
    		InputStream is = new java.io.FileInputStream(new File(path + filename));
    		props.load(is);
    		is.close();
    		props.put("system.path", sysPath);
    		return props;
    	}
    
    	public String getConfPath() throws Exception
    	{
    		if (confPath != null)
    			return confPath;
    		sysPath = sysPath();
    		confPath = sysPath + "conf" + File.separator;
    		return confPath;
    	}
    
    	public String getSysPath() throws Exception
    	{
    		if (sysPath != null)
    			return sysPath;
    		sysPath = sysPath();
    		confPath = sysPath + "conf" + File.separator;
    		return sysPath;
    	}
    
    	public String getWebPath() throws Exception
    	{
    		if (webPath != null)
    			return webPath;
    		sysPath();
    		return webPath;
    	}
    
    	private String sysPath() throws Exception
    	{
    		ClassLoader cl = this.getClass().getClassLoader();
    		String classname = this.getClass().getName().replace('.', '/') + ".class";
    		String res = null;
    		if (cl != null)
    		{
    			java.net.URL url = cl.getResource(classname);
    			if (url != null)
    			{
    				String path = url.getFile();
    				int fileStrPosition = path.indexOf("file:/");
    				int begin = 0;
    				int end = path.length();
    				if (fileStrPosition >= 0)
    					begin = fileStrPosition + 5;
    				end = path.indexOf("WEB-INF/");
    				if (end > 0)
    				{
    					String rf = path.substring(begin, end);
    					webPath = rf;
    					File f = new File(rf + "WEB-INF/conf/");
    					if (f.exists())
    						res = new File(rf + "WEB-INF/").getAbsolutePath() + File.separator;
    					else
    						res = new File(rf).getParentFile().getAbsolutePath() + File.separator;
    				} else
    				{ 
    					res = new File(".").getAbsolutePath();
    					res = res.substring(0, res.length() - 1);
    				}
    			}
    		}
    		return java.net.URLDecoder.decode(res, "UTF-8");
    	}
    
    	public Properties readXML(String xmlName) throws Exception
    	{
    		this.filename = xmlName;
    		return readXML();
    	}
    	
    	public Properties readXML()throws Exception{
    		String path = getConfPath();
    		Properties props = new Properties();
    		InputStream is = new java.io.FileInputStream(new File(path + filename));
    		props.loadFromXML(is);
    		is.close();
    		//props.put("system.path", sysPath);
    		return props;
    	}
    	public void storeXML(Properties prop)throws Exception{
    		String path = getConfPath();
    		prop.storeToXML(new FileOutputStream(new File(path + filename)), "Store By Program");
    	}
    	
    	public static void main(String[] args) throws Exception
    	{
    		SysConf sc = new SysConf("log4j.conf");
    		System.out.println(sc.read());
    	}
    }
java中关于String的操作有很多。而String中也有很多的API，但是还远远不够。
比方说：
 - 不区分大小写的比较
 - 不区分大小写的查找子串
 - ......

所以，封装了下面的这个：

    import java.security.MessageDigest;
    import java.security.NoSuchAlgorithmException;
    import java.util.StringTokenizer;
    import java.util.regex.Matcher;
    import java.util.regex.Pattern;
    
    public class StringUtil
    {
    	public static String data2(String s)
    	{
    		if (s == null)
    			return null;
    
    		MessageDigest md = null;
    		try
    		{
    			md = MessageDigest.getInstance("MD5");
    		} catch (NoSuchAlgorithmException e)
    		{
    			return null;
    		}
    
    		return toHex(md.digest(s.getBytes()));
    	}
    
    	private static String toHex(byte buffer[])
    	{
    		StringBuffer sb = new StringBuffer(32);
    		String s = null;
    		for (int i = 0; i < buffer.length; i++)
    		{
    			s = Integer.toHexString((int) buffer[i] & 0xff);
    			if (s.length() < 2)
    				sb.append('0');
    			sb.append(s);
    		}
    		return sb.toString();
    	}
    
    	public static String[] split(String str, String s)
    	{
    		if (str == null)
    			return null;
    
    		if (s == null)
    			return new String[] { str };
    
    		StringTokenizer st = new StringTokenizer(str, s);
    		String[] r = new String[st.countTokens()];
    		int i = 0;
    		while (st.hasMoreTokens())
    			r[i++] = st.nextToken();
    		return r;
    	}
    
    	public static int indexOfIgnoreCase(String str, char ch)
    	{
    		return indexOfIgnoreCase(str, 0, ch);
    	}
    
    	public static int indexOfIgnoreCase(String str, int fromIndex, char ch)
    	{
    		if (str == null || str.length() == 0)
    			return -1;
    
    		if (fromIndex >= str.length())
    			return -1; // Note: fromIndex might be near -1>>>1.
    
    		if (fromIndex < 0)
    			fromIndex = 0;
    
    		for (int i = fromIndex; i < str.length(); i++)
    		{
    			if (StringUtil.equalsIngoreCase(ch, str.charAt(i)))
    				return i;
    		}
    		return -1;
    	}
    
    	public static int indexOfIgnoreCase(String str, String target)
    	{
    		return indexOfIgnoreCase(str, 0, target);
    	}
    
    	public static int indexOfIgnoreCase(String str, int fromIndex, String target)
    	{
    		if (str == null || str.length() == 0 || target == null || target.length() == 0)
    			return -1;
    
    		if (fromIndex >= str.length())
    			return -1;
    
    		if (fromIndex < 0)
    			fromIndex = 0;
    
    		char first = target.charAt(0);
    		int max = str.length() - target.length();
    
    		for (int i = fromIndex; i <= max; i++)
    		{
    			if (!equalsIngoreCase(str.charAt(i), first))
    			{
    				while (++i <= max && !equalsIngoreCase(str.charAt(i), first))
    				{
    				}
    			}
    			if (i <= max)
    			{
    				int j = i + 1;
    				int end = j + target.length() - 1;
    				for (int k = 1; j < end && equalsIngoreCase(str.charAt(j), target.charAt(k)); j++, k++)
    				{
    				}
    				if (j == end) // Found whole string.
    					return i;
    			}
    		}
    
    		return -1;
    	}
    
    	/**
    	 * 返回第一次匹配正则表达式的串
    	 * @param str
    	 * @param regexStr
    	 * @return
    	 */
    	public static String firstMatchStr(String str, String regexStr)
    	{
    		Pattern p = Pattern.compile(regexStr);
    		Matcher m = p.matcher(str);
    
    		if (m.find())
    			return m.group();
    		return null;
    	}
    
    	public static boolean equalsIngoreCase(char c1, char c2)
    	{
    		if (c1 == c2)
    			return true;
    
    		// If characters don't match but case may be ignored,
    		// try converting both characters to uppercase.
    		// If the results match, then return true
    		char u1 = Character.toUpperCase(c1);
    		char u2 = Character.toUpperCase(c2);
    		if (u1 == u2)
    			return true;
    		// Unfortunately, conversion to uppercase does not work properly
    		// for the Georgian alphabet, which has strange rules about case
    		// conversion. So we need to make one last check before
    		// exiting.
    		return (Character.toLowerCase(u1) == Character.toLowerCase(u2));
    	}
    
    	public static String addMarkIgnoreCase(String str, char r, String beginMark, String endMark)
    	{
    		if (str == null || str.length() == 0)
    			return str;
    		StringBuffer strb = new StringBuffer(str.length());
    		for (int i = 0; i < str.length(); i++)
    		{
    			char c = str.charAt(i);
    
    			if (equalsIngoreCase(c, r))
    				strb.append(beginMark).append(c).append(endMark);
    			else
    				strb.append(c);
    		}
    		return strb.toString();
    	}
    
    	public static String addMarkIgnoreCase(String str, String r, String beginMark, String endMark)
    	{
    		if (str == null || str.length() == 0 || r == null || r.length() == 0)
    			return str;
    
    		int p = indexOfIgnoreCase(str, r); // 找到被取代串的位置
    		if (p == -1)
    			return str;
    
    		int last = 0;
    		StringBuffer strb = new StringBuffer(str.length() << 1); // 声明一个StringBuffer,
    		// 长度是 参数1
    		// 字符串的两倍
    
    		while (p >= 0)
    		{
    			strb.append(str.substring(last, p));
    			strb.append(beginMark);
    			strb.append(str.substring(p, p + r.length()));
    			strb.append(endMark);
    
    			last = p + r.length();
    			p = indexOfIgnoreCase(str, last, r);
    		}
    		return strb.append(str.substring(last)).toString();
    	}
    
    	/**
    	 * replace r to t from str
    	 * @param str
    	 * @param r
    	 * @param t
    	 * @return
    	 */
    	public static String replace(String str, char r, char t)
    	{
    		if (str == null)
    			return str;
    		StringBuffer strb = new StringBuffer(str.length());
    		for (int i = 0; i < str.length(); i++)
    		{
    			char c = str.charAt(i);
    			if (c == r)
    				c = t;
    			strb.append(c);
    		}
    		return strb.toString();
    	}
    
    	/**
    	 * replace r to t from str
    	 * @param str
    	 * @param r
    	 * @param t
    	 * @return
    	 */
    	public static String replace(String str, String r, String t)
    	{
    		if (str == null || r == null || t == null)
    			return str;
    		if (str.trim().length() == 0 || r.length() == 0)
    			return str;
    		int p = str.indexOf(r); // 找到被取代串的位置
    		if (p == -1)
    			return str;
    
    		int last = 0;
    		StringBuffer strb = new StringBuffer(str.length() << 1); // 声明一个StringBuffer,
    		// 长度是 参数1
    		// 字符串的两倍
    
    		while (p >= 0)
    		{
    			strb.append(str.substring(last, p));
    			if (t != null)
    				strb.append(t);
    			last = p + r.length();
    			p = str.indexOf(r, last);
    		}
    		return strb.append(str.substring(last)).toString();
    	}
    
    	public static boolean isEn(String target)
    	{
    		for (int i = 0; i < target.length(); i++)
    		{
    			if (!isLetter(target.charAt(i)))
    				return false;
    		}
    		return true;
    	}
    
    	public static boolean isRegex(String str)
    	{
    		if ((str.indexOf('*')) != -1 || (str.indexOf('?')) != -1)
    			return true;
    		return false;
    	}
    
    	public static boolean isLetter(char ch)
    	{
    		if ((ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z'))
    			return true;
    		return false;
    	}
    
    	 public static void main(String[] args)
    	 {
    		 String s1 = "abc abc";
    		 String s2 = "中国";
    		 System.out.println(StringUtil.isEn(s1));
    		 System.out.println(StringUtil.isEn(s2));
    		 s1 = StringUtil.replace(s1, " ", "");
    		 System.out.println(s1);
    		String str = "123women大家都。3";
    		char ch = 'W';
    		String t = "mEN";
    		System.out.println(StringUtil.indexOfIgnoreCase(str, 3, ch));
    		System.out.println(StringUtil.indexOfIgnoreCase(str, 0, t));
    		System.out.println(StringUtil.addMarkIgnoreCase(str, ch, "<div>", "</div>"));
    		System.out.println(StringUtil.addMarkIgnoreCase(str, t, "<div>", "</div>"));
    	 }
    }
进行网络爬虫下载的时候，可能由于对方的网页做得不规范，使得字符集是错误的。

为了解决这个问题，我们需要对字符集进行一个简单的探测。因为主要抓取的是国内的中文和国外的英文网站。

所以，下面的代码也只能分析出这两种：

[ByteBuffer 来自这][1]


    import ByteBuffer;
    
    public class CharsetUtil
    {
    	public static boolean isUtf8(ByteBuffer content)
    	{
    		double len = (double) content.getUsed();
    		byte[] bb = content.array();
    		double number = 0D;
    		for (int i = 0; i < len; i++)
    		{
    			if (isUtf8(bb[i]))
    				number++;
    		}
    
    		if (number / 99 * 100 >= len)
    			return true;
    
    		return false;
    	}
    
    	public static boolean isUtf8(byte b)
    	{
    		if ((b & 0x80) == 0)
    			return true;
    		if ((b & 0xc0) == 0x80)
    			return true;
    		if ((b & 0xe0) == 0xc0)
    			return true;
    		if ((b & 0xf0) == 0xe0)
    			return true;
    		return false;
    	}
    }

  [1]: /blogs/12
