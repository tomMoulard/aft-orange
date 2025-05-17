locals {
  common_lambda_config = {
    runtime      = "python3.9"
    timeout      = 30
    memory_size  = 256
    architecture = ["x86_64"]
  }
  
  lambda_functions = {
    create_account = {
      handler      = "handlers.account_handlers.create_account_handler"
      description  = "Handler for account creation requests"
    },
    update_account = {
      handler      = "handlers.account_handlers.update_account_handler"
      description  = "Handler for account update requests"
    },
    delete_account = {
      handler      = "handlers.account_handlers.delete_account_handler"
      description  = "Handler for account deletion requests"
    },
    upgrade_account = {
      handler      = "handlers.account_handlers.upgrade_account_handler"
      description  = "Handler for account upgrade requests"
    },
    downgrade_account = {
      handler      = "handlers.account_handlers.downgrade_account_handler"
      description  = "Handler for account downgrade requests"
    },
    add_option = {
      handler      = "handlers.account_handlers.add_option_handler"
      description  = "Handler for adding options to an account"
    },
    remove_option = {
      handler      = "handlers.account_handlers.remove_option_handler"
      description  = "Handler for removing options from an account"
    },
    authorizer = {
      handler      = "handlers.auth_handler.lambda_authorizer"
      description  = "JWT token authorizer for API Gateway"
    }
  }
} 