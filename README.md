# Goal 🎯
Project Request Manager🚀 

This project has the primary goal of manage requisitions to a specific endpoint and treat different errors from the lib requests.
The class will try a couple of times until the result is the wanted response or it hits the maximum number of tries

# Used technologies 💻
    * Requests
    * Python

# Installation ⚙
To run the project, follow the next steps

  * Intall virtualenv
  ```sh
  pip install virtualenv
  ```
  * Create a virtual enviroment
  ```sh
  virtualenv venv 
  ```

  * Enter the virtual enviroment
  ```sh
  venv/Scripts/activate
  ```

# Implementing the class


Import the class to your project and add it as a super class or create a object from the class

```
from request_manager.manager import RequestManager

class my_class(RequestManager):
    def __init__(self):
        super(my_class, self).__init__()
```

```
from request_manager.manager import RequestManager

object = RequestManager()
object.send_requisitons_request()
```

# Files Structure

## Librarys📚

### **request**
Class used to make requests using the urllib as a basic manager
