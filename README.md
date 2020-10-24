# Flask tutorial

1. Followed official flask site [here](https://flask.palletsprojects.com/en/1.1.x/tutorial)
## Installing Flask and dependencies

  `source /opt/conda/bin/activate` 


  `conda create -n flask -c conda-forge python=3.8.6 flask=1.1.2`


  `conda activate flask`


  For version checks of  flask and python (`-E` for extended REGEX and `-w` for complete match words only)


  `conda list | grep -Ew 'python|flask' `

## Application Setup

### Application Factory
Instead of creating a **Flask** instance globally, you will create it inside a function. This function is known as the *application factory*. Any configuration, registration, and other setup the application needs will happen inside the function, then the application will be returned.


