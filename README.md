# Protection of Sensitive Data: Creating, Analyzing and Testing Protocols of Differential Privacy

The problem of preserving privacy while extracting information during data analysis, has been an everlasting one. Specifically, during the big­data era, user details can be easily compromised by a malicious handler, something considered both as a security, and as a privacy issue.

The optimal fix to the subject, is Differential Privacy, which is actually a promise, made by the data handler to the user, that they will not be affected, by allowing their data to be used in any analysis, no matter what other stud­ies/databases/info resources are available. Meanwhile, the output data statistics should be accurate enough for any researcher to extract useful information from them.

The goal of this thesis, is to examine and compare previously created mechanisms for D.P., while also creating our own mechanism, that serves to the purpose of achieving Local D.P., a form of Differential Privacy that is nowadays widely used in machine learning algorithms, aiming to protect the individuals that send their personal data for analysis. We will do so, by creating a library that is easy to use, and applies to all the rules of data privacy, and then extract conclusions from its use.

## Analyzing and Testing of existing protocols

The first two chapters of the thesis are dedicated in testing libraries created, like the **IBM diffprivlib** and the **ARX Tool**. The directory  `ibm_lib_work` contains notebooks for testing the IBM library, and the directory `ARX_work`, contains Java code created in order to test the ARX API. 

## Creating an LDP protocol

Local Differential Privacy (LDP), is a modern form of DP used in many real world application. The main downside of most LDP protocols, is their lack of efficiency when a small number of users contribute in the protocol. During this thesis, we aim to create a protocol to fix this probem, and we are introducing the **Distance Sensitive** protocol, which fufils exactly that promise. We conduct testings, and comparisons with other LDP protocols, which were implemented using Python. All our LDP work can be found in the directory `LDP`.
