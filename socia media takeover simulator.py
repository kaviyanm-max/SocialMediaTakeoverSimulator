
import time
try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except Exception:
    print("tkinter not available. Install tkinter or run on desktop Python.")
    raise

USERS={'user1':{'password':'pass123'}}

class App:
    def __init__(self, root):
        self.root=root
        self.root.title("Social Media Account Takeover Simulator")
        self.root.geometry("900x600")
        self.risk=0; self.attempts=0; self.locked=False
        self.build()

    def build(self):
        tk.Label(self.root,text="Social Media Account Takeover Simulator",font=("Arial",18,"bold")).pack(pady=10)
        frame=tk.Frame(self.root); frame.pack(fill='x',padx=10)
        left=tk.LabelFrame(frame,text="Attack Panel"); left.pack(side='left',fill='both',expand=True,padx=5)
        right=tk.LabelFrame(frame,text="Defense Panel"); right.pack(side='left',fill='both',expand=True,padx=5)
        tk.Label(left,text="Username").grid(row=0,column=0); self.u=tk.Entry(left); self.u.grid(row=0,column=1); self.u.insert(0,"user1")
        tk.Label(left,text="Password").grid(row=1,column=0); self.p=tk.Entry(left,show="*"); self.p.grid(row=1,column=1)
        tk.Button(left,text="Stolen Credential Login",command=self.login).grid(row=2,column=0,columnspan=2,sticky='ew')
        tk.Button(left,text="Unknown Device Login",command=self.device).grid(row=3,column=0,columnspan=2,sticky='ew')
        tk.Button(left,text="OTP Interception",command=self.otp).grid(row=4,column=0,columnspan=2,sticky='ew')
        tk.Button(left,text="Suspicious Location",command=self.geo).grid(row=5,column=0,columnspan=2,sticky='ew')

        self.mfa=tk.BooleanVar(value=True); self.alert=tk.BooleanVar(value=True); self.lockout=tk.BooleanVar(value=True)
        tk.Checkbutton(right,text="Enable MFA",variable=self.mfa).pack(anchor='w')
        tk.Checkbutton(right,text="Enable Alerts",variable=self.alert).pack(anchor='w')
        tk.Checkbutton(right,text="Smart Lockout",variable=self.lockout).pack(anchor='w')
        tk.Button(right,text="Reset",command=self.reset).pack(fill='x')

        self.pb=ttk.Progressbar(self.root,maximum=100); self.pb.pack(fill='x',padx=10,pady=5)
        self.log=tk.Text(self.root,height=20); self.log.pack(fill='both',expand=True,padx=10,pady=10)
        self.write("System ready.")

    def write(self,msg):
        self.log.insert('end',time.strftime("%H:%M:%S ")+msg+"\n"); self.log.see('end')

    def risk_add(self,v):
        self.risk=min(100,self.risk+v); self.pb['value']=self.risk

    def login(self):
        if self.locked: return
        if self.u.get() in USERS and USERS[self.u.get()]['password']==self.p.get():
            self.write("[ATTACK] Correct credentials used.")
            self.risk_add(20)
            if self.mfa.get(): self.write("[DEFENSE] MFA blocked access.")
            else: self.write("[BREACH] Account takeover successful.")
        else:
            self.attempts+=1; self.write("[ATTACK] Invalid credentials.")
            self.risk_add(10)
            if self.lockout.get() and self.attempts>=3:
                self.locked=True; messagebox.showwarning("Locked","Account locked")

    def device(self): self.write("[ATTACK] Unknown device login."); self.risk_add(15)
    def otp(self): self.write("[ATTACK] OTP interception attempt."); self.risk_add(25)
    def geo(self):
        self.write("[ATTACK] Suspicious location login."); self.risk_add(20)
        if self.alert.get(): self.write("[DEFENSE] Alert sent to user.")
    def reset(self):
        self.risk=0; self.attempts=0; self.locked=False; self.pb['value']=0
        self.log.delete('1.0','end'); self.write("System reset.")

root=tk.Tk()
App(root)
root.mainloop()
