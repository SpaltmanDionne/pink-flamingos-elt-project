#Terraform block: define required providers
terraform {
  required_providers {
    <provider-name> = {
      source  = "<provider-source>"
      version = "<version-constraint>"
    }
  }
}

# Provider configuration
provider "<provider-name>" {
  # provider-specific configuration
}

# Module declarations
module "<module1-name>" {
  source = "<module1-source>"
  # module-specific input variables
}

module "<module2-name>" {
  source = "<module2-source>"
  # module-specific input variables
  <input-variable> = module.<module1-name>.<output-variable>
}

module "<module3-name>" {
  source = "<module3-source>"
  # module-specific input variables
  <input-variable> = module.<module1-name>.<output-variable>
}

module "<module4-name>" {
  source = "<module4-source>"
  # module-specific input variables
  <input-variable1> = module.<module1-name>.<output-variable>
  <input-variable2> = module.<module2-name>.<output-variable>
}

