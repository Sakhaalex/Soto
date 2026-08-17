# File Operations Co-pilot
## Abstract
I want to create a file log dictionary which will be auto-updated when I start the computer or when I press manually the switch the csv structure would be storing majorly two parameters i.e. Path and Folder and rest 16K nearly will be files. So, when the user will press or add the folder into directory it's path will be noted and it will note name of all the files and folders till it encounters folders which will be noted at the last there will be no parameter as such it will be under same parameter just in increasing order like F1,F2..etc but before ending the folders will be at last. So that in case a path contains a folder which contain sub-folders and files , we can have a denotation * before names of folders in the rows to make a distinction between files and folders, so in case we need a file the program will go through the folder row it will then check the * folders which will be pointing to another row of folder so this process will be done until the file is found. 

## Problem Statement
It is tedious job for a PC in an OS like windows to search every file and folder present , this system will help maintaining a file log dictionary across the user selected paths , it will be more convenient for the user to check a csv file than making the PC do it. 

## Objectives
User can simply maintain the log of all the files with their extensions and their exact locations so it should be pretty easy to find the new files, old files, filter the type of file data the user wants to find.
System commands will be running through a simple GUI so the user will be using them as a simple mechanism to get details of program without needing much info of the right program for file operations. In short, all kinds of file operations are on the user's hand, the extension of it is in the future scope of the project
In case the user wants to recreate the same folder structure the user can instantly do it wherever he/she wants can do it on a click because only the folder will be noted in the directory.
The alias of the file names will be as it is so the extension filtering will be far easier, i.e. how many extensions of how many files are there will be completely noted i.e. the user will get to know how many pdfs, docs, md, etc  are there , in short a statistics will be far easier
Not only segregation but file moving can be one of the biggest advantages. E.g. If u have a downloads folder messy with all data types pdfs,word docs,etc you want to arrange it according to it's extension , you can simply add that path to this program/system then simply on one click the program will create the folders of new extensions and will transfer those files at their necessary place.
The same can be done based on various filters like size, date, etc 
Optional things like file info, version change, etc can be done but it is already being done in the system so the program can just find it easily for the user. 
File deletion: In case any file is deleted then the system will mark it with some different notation  and rename it with mention of it's time log so that the user can know in case the file is deleted.

## Implementation
- There will be one csv as File.csv which will contain the folder names and path for convenience. The folder names which will be inside folder row will have notation like * and the parameters will be incremental so that the files in any folder will have atleast a limit of 16K something.
- It will use basic system commands to retreive file info,path,alias of file,etc so once the user clicks to update or it should be automatically run the script to update the path once the system is started to get the latest file info ,names, etc in the csv
- It will have tools to help user segregate transfer the files, folders into new locations( robocopy commands will be help), create new folders that can be according to extension,date,file size,etc to help user with file operations, other basic file informations, copy folder structure to clone similar ones, create bat files for the same, etc
- Browsing is the biggest option for path u don't need to paste it traditionally use UI to browse through the paths, folders,etc to add them in the csv
 
### UI details
- The system will be have a GUI in CSS or advanced having a simple search option to search the file or folder with necessary filter like file type,etc
- GUI look should be highly enhanced and other options in the readme file should be done without any mention e.g. file details, versions, how many types of extensions with quantity exist in the path, a tree like strucutre we see in any IDE in sideways but in GUI with some good colour combinations (same hiefnation structure nothing much fancy needed ), adding a path/folder, etc
- There will be simple white background with blue coloured search bar.
- There will be a side panel to control filters
- Else information will be presented down the space available
- The path with the tree look with colourful should be an optional sidebar kinda thing to open or see the directory
- When search completed there will be a big icon to show the file so the user clicks it and it opens in real
- Arrange all these details into one html page so that the user when runs program defaultly runs into the default browser (brave), reason being we are thinking of integrating more such csv based systems into the system and if everything will have it's own page then we can simply integrate it.
- The search bar will be at top and will be big enough to see the user searching it

### Limitation
Current limitation can be the rows limit in excel which can be 10 lakh something but in case it is near to end the last row will end as CHN and the respective path of the next csv in this way we will be creating a CHAIN of csvs to maintatin this file log dictionary.

## Future Scope
- It can be seen as added feature or plugin with another program or system to help it with the files and their operations
- It can be used to detect deleted files and folders with exact paths
- Once it can be attached to a powerful automation system all the files across the system will be controlled through the automation system or co-pilot. It will help the system control maximum of files and folders.

# File Operations Co-pilot
## Abstract
I want to create a file log dictionary which will be auto-updated when I start the computer or when I press manually the switch the csv structure would be storing majorly two parameters i.e. Path and Folder and rest 16K nearly will be files. So, when the user will press or add the folder into directory it's path will be noted and it will note name of all the files and folders till it encounters folders which will be noted at the last there will be no parameter as such it will be under same parameter just in increasing order like F1,F2..etc but before ending the folders will be at last. So that in case a path contains a folder which contain sub-folders and files , we can have a denotation * before names of folders in the rows to make a distinction between files and folders, so in case we need a file the program will go through the folder row it will then check the * folders which will be pointing to another row of folder so this process will be done until the file is found. 

## Problem Statement
It is tedious job for a PC in an OS like windows to search every file and folder present , this system will help maintaining a file log dictionary across the user selected paths , it will be more convenient for the user to check a csv file than making the PC do it. 

## Objectives
User can simply maintain the log of all the files with their extensions and their exact locations so it should be pretty easy to find the new files, old files, filter the type of file data the user wants to find.
System commands will be running through a simple GUI so the user will be using them as a simple mechanism to get details of program without needing much info of the right program for file operations. In short, all kinds of file operations are on the user's hand, the extension of it is in the future scope of the project
In case the user wants to recreate the same folder structure the user can instantly do it wherever he/she wants can do it on a click because only the folder will be noted in the directory.
The alias of the file names will be as it is so the extension filtering will be far easier, i.e. how many extensions of how many files are there will be completely noted i.e. the user will get to know how many pdfs, docs, md, etc  are there , in short a statistics will be far easier
Not only segregation but file moving can be one of the biggest advantages. E.g. If u have a downloads folder messy with all data types pdfs,word docs,etc you want to arrange it according to it's extension , you can simply add that path to this program/system then simply on one click the program will create the folders of new extensions and will transfer those files at their necessary place.
The same can be done based on various filters like size, date, etc 
Optional things like file info, version change, etc can be done but it is already being done in the system so the program can just find it easily for the user. 
File deletion: In case any file is deleted then the system will mark it with some different notation  and rename it with mention of it's time log so that the user can know in case the file is deleted.

## Implementation
- There will be one csv as File.csv which will contain the folder names and path for convenience. The folder names which will be inside folder row will have notation like * and the parameters will be incremental so that the files in any folder will have atleast a limit of 16K something.
- It will use basic system commands to retreive file info,path,alias of file,etc so once the user clicks to update or it should be automatically run the script to update the path once the system is started to get the latest file info ,names, etc in the csv
- It will have tools to help user segregate transfer the files, folders into new locations( robocopy commands will be help), create new folders that can be according to extension,date,file size,etc to help user with file operations, other basic file informations, copy folder structure to clone similar ones, create bat files for the same, etc
- Browsing is the biggest option for path u don't need to paste it traditionally use UI to browse through the paths, folders,etc to add them in the csv
 
### UI details
- The system will be have a GUI in CSS or advanced having a simple search option to search the file or folder with necessary filter like file type,etc
- GUI look should be highly enhanced and other options in the readme file should be done without any mention e.g. file details, versions, how many types of extensions with quantity exist in the path, a tree like strucutre we see in any IDE in sideways but in GUI with some good colour combinations (same hiefnation structure nothing much fancy needed ), adding a path/folder, etc
- There will be simple white background with blue coloured search bar.
- There will be a side panel to control filters
- Else information will be presented down the space available
- The path with the tree look with colourful should be an optional sidebar kinda thing to open or see the directory
- When search completed there will be a big icon to show the file so the user clicks it and it opens in real
- Arrange all these details into one html page so that the user when runs program defaultly runs into the default browser (brave), reason being we are thinking of integrating more such csv based systems into the system and if everything will have it's own page then we can simply integrate it.
- The search bar will be at top and will be big enough to see the user searching it

### Limitation
Current limitation can be the rows limit in excel which can be 10 lakh something but in case it is near to end the last row will end as CHN and the respective path of the next csv in this way we will be creating a CHAIN of csvs to maintatin this file log dictionary.

## Future Scope
- It can be seen as added feature or plugin with another program or system to help it with the files and their operations
- It can be used to detect deleted files and folders with exact paths
- Once it can be attached to a powerful automation system all the files across the system will be controlled through the automation system or co-pilot. It will help the system control maximum of files and folders.
