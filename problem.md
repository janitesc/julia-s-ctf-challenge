# julia challenge


- Type: custom
- Category: Forensics
- Points: 50
- Namespace: 18739


## Description

We have captured a memory dump from a process that deleted a file.  
You are given a file called {{url_for('memdump.bin', 'here')}}.

Download {{url_for('memdump.bin', 'here')}}, inspect it, and recover the contents of the deleted flag file.  
Submit the recovered flag as your answer.

to make the chalenge more fun(ie for problem dev 2): 
hide the flag more subtly, add encoding(i wanted to AES encrypt it), maybe try to add a more realistic memdump setup if I have time. I want to do something similar to this: https://medium.com/@chaoskist/cyberspacectf-2024-memory-forensic-challenge-35d1ea05ea33
where you have an "evil" process that is deleting a file and you have to do memdump analysis (similar to the CTF from class but you have to read a memdump and not a network transfer)