# Hey and welcome to the installation of the CipherFinder via Powershell
### This Script will
- Install Python3.12
- Add Python to the Path variable
- Install the FivemCipherFinder package for you
### This Script will not
- Remove any ciphers (this is the job of the finder)
- Bake Cookies for you

As said above, this script is just to install it, I've created it to make the Process simpler for non-tech people that might encounter problems.

## Install
### How to get it
The installation script is a **standalone**, that means you can just download that single script and run it.

- get the script [here](https://github.com/exersalza/FivemCipherFinder/blob/main/install.ps1)
  - just press on that download button there.

    ![img.png](img.png)

Press right-click on the file and click on "run with powershell"


## Troubleshooting

Should you encounter `cannot be loaded because running scripts is disabled on this system. For more information, see about_Execution_Policies at` 

Type **one** of the following commands that fits to your needs:


You can change the execution policy using the Set-ExecutionPolicy cmdlet in PowerShell. For example, to change the policy to RemoteSigned, you would use the following command:

- `Set-ExecutionPolicy RemoteSigned`

You will need to run PowerShell as an administrator to change the execution policy. If you want to change the policy only for the current user, you can add the -Scope CurrentUser parameter to the command:

- `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

If you want to bypass the execution policy for a single script without changing the policy, you can do so with the -ExecutionPolicy Bypass parameter when running the script:

- `powershell -ExecutionPolicy Bypass -File install.ps1`

Please note that the execution policy is a safety feature, and it's important to understand the implications of changing it. You should only run scripts that you trust