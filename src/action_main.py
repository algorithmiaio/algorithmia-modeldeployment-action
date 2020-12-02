#!/usr/bin/python3

import os
import algorithmia_deployer
import notebook_executor


if __name__ == "__main__":
    workspace = os.getenv("GITHUB_WORKSPACE")
    git_repo = os.getenv("GITHUB_REPOSITORY")
    git_ref = os.getenv("GITHUB_REF")
    commit_SHA = os.getenv("GITHUB_SHA")
    commit_msg = os.getenv("HEAD_COMMIT_MSG")
    algorithmia_api_key = os.getenv("INPUT_ALGORITHMIA_API_KEY")
    algorithmia_username = os.getenv("INPUT_ALGORITHMIA_USERNAME")
    algorithmia_algo_name = os.getenv("INPUT_ALGORITHMIA_ALGONAME")
    notebook_path = os.getenv("INPUT_NOTEBOOK_PATH")
    model_path = os.getenv("INPUT_MODEL_PATH")
    upload_path = os.getenv("INPUT_ALGORITHMIA_UPLOADPATH")
    algorithmia_api = os.getenv("INPUT_ALGORITHMIA_API")

    error_template_str = "Field '{}' not defined in workflow file. Please check your workflow configuration"
    if not algorithmia_api_key:
        raise Exception(error_template_str.format("algorithmia_api_key"))
    if not algorithmia_username:
        raise Exception(error_template_str.format("algorithmia_username"))
    if not algorithmia_algo_name:
        raise Exception(error_template_str.format("algorithmia_algoname"))
    if not upload_path:
        raise Exception(error_template_str.format("algorithmia_uploadpath"))
    if not model_path:
        raise Exception(error_template_str.format("model_path"))

    if os.path.exists(workspace):
        try:
            notebook_executor = notebook_executor.NotebookExecutor(
                workspace, notebook_path
            )
            notebook_executor.run()

            algorithmia_deployer = algorithmia_deployer.AlgorithmiaDeployer(
                api_key=algorithmia_api_key,
                api_address=algorithmia_api,
                username=algorithmia_username,
                algo_name=algorithmia_algo_name,
                model_path=model_path,
                workspace_path=workspace,
            )
            algorithmia_deployer.upload_and_link_algo_model(
                upload_path=upload_path,
                git_repo=git_repo,
                git_ref=git_ref,
                commit_SHA=commit_SHA,
                commit_msg=commit_msg,
            )
        except Exception as e:
            raise e
    else:
        raise Exception(
            "actions/checkout action should be run on the main repository, before this action. Please check your workflow configuration."
        )
