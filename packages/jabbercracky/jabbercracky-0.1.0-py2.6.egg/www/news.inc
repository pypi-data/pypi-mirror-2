<br/>
<b>awgh's hash cracker</b>
<br/>
<br/>
This hash-cracking service is provided free of charge for users of ChaosVPN.  
No login needed, but the results are public.  Chaos, indeed ;)
<br/>
This cracker will first attempt to look up your hash using our LaRGe set of rainbow tables...
<br/>
<br/>
<b>NEW FEATURE</b> (for md5 hashes only)
<br/>
If the rainbow tables fail, the service will now brute-force md5 hashes GPU-accelerated by the server's Quadro FX 1800.
<br/>
It looks like this is actually faster than the tables for md5, so maybe I will make it the first pass someday...
<br/>
<br/>
There is a limit to <strong>5 submitted hashes per hour</strong> per IP address.
<br/>
<br/>
Also, please note that for LM the cracker will only accept 16 characters.  
<br/>
<br/>
If you have a LanMan hash, simply submit the first and second halves of the LanMan hash as <strong>separate jobs</strong>.
<br/>
<br/>
Currently supported rainbow tables are:
<br/>
<ul>
<li>MD5
    <ul>
        <li>alpha-numeric-space 1-8 chars</li>
        <li>alpha-space 1-9 chars</li>
        <li>loweralpha-numeric-space 1-8 chars</li>
        <li>loweralpha-numeric-symbol32-space 1-7 chars</li>
    </ul>
</li>
<br/>
<li>LM
    <ul><li>All Chars 1-8 Chars (Full Set)</li></ul>
</li>
<br/>
<li>HalfLM Challenges
    <ul><li>alpha-numeric 1-7 chars</li></ul>
</li>
<br/>
<li>NTLM
    <ul>
      <li>alpha-numeric-space 1-8 chars</li>
      <li>alpha-space 1-9 chars</li>
      <li>hybrid</li>
      <li>loweralpha-numeric-space 1-8 chars</li>
      <li>loweralpha-numeric-symbol32-space 1-7 chars</li>
      <li>loweralpha-space 1-9 chars</li>
      <li>mixalpha-numeric 1-8 chars</li>
    </ul>
</ul>
<br/>
<br/>
Cracking times range from a couple minutes for LM to 15 minutes sometimes for MD5, but there is some possibility for performance improvement there.
<br/>
I am currently working on packaging up all of this code for release!  Bugs/flames to awgh@awgh.org
<br/>
<br/>
Thanks to the ChaosVPN and happy cracking!
<br/><br/>
- awgh
