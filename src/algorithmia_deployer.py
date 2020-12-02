import Algorithmia
import os
import json
from datetime import datetime
import hashlib


class AlgorithmiaDeployer:
    def __init__(
        self, api_key, api_address, username, algo_name, model_path, workspace_path,
    ) -> None:
        self.algo_client = Algorithmia.client(api_key, api_address)
        self.username = username
        self.algo_name = algo_name
        self.model_path = model_path
        self.workspace_path = workspace_path

        self.model_full_path = f"{workspace_path}/{model_path}"

    def upload_and_link_algo_model(
        self, upload_path, git_repo, git_ref, commit_SHA, commit_msg
    ):
        if os.path.exists(self.model_full_path):
            model_md5_hash = self._calculate_model_md5()
            if model_md5_hash:
                upload_path = self._replace_placeholders(upload_path)
                algorithmia_upload_path = self._upload_model(upload_path, commit_SHA)
                if algorithmia_upload_path:
                    self._update_algo_model_manifest(
                        git_repo=git_repo,
                        git_ref=git_ref,
                        commit_SHA=commit_SHA,
                        commit_msg=commit_msg,
                        model_filepath=algorithmia_upload_path,
                        model_md5_hash=model_md5_hash,
                    )
                else:
                    raise Exception(
                        "Could not upload model file to Algorithmia. Stopping the workflow execution."
                    )
            else:
                raise Exception(
                    "Could not calculate model file hash. Stopping the workflow execution."
                )
        else:
            raise Exception(
                f"Model file not found at {self.model_full_path}. Please check your workflow configuration."
            )

    def _replace_placeholders(self, parametric_str):
        if "$ALGORITHMIA_USERNAME" in parametric_str:
            print(f"Replacing $ALGORITHMIA_USERNAME in {parametric_str}")
            parametric_str = parametric_str.replace(
                "$ALGORITHMIA_USERNAME", self.username
            )
        if "$ALGORITHMIA_ALGONAME" in parametric_str:
            print(f"Replacing $ALGORITHMIA_ALGONAME in {parametric_str}")
            parametric_str = parametric_str.replace(
                "$ALGORITHMIA_ALGONAME", self.algo_name
            )
        print(f"Replaced string became: {parametric_str}")
        return parametric_str

    def _calculate_model_md5(self):
        DIGEST_BLOCK_SIZE = 128 * 64
        md5_hash = None
        try:
            with open(self.model_full_path, "rb") as f:
                file_hash = hashlib.md5()
                while chunk := f.read(DIGEST_BLOCK_SIZE):
                    file_hash.update(chunk)
            md5_hash = file_hash.hexdigest()
        except Exception as e:
            print(f"An exception occurred while getting MD5 hash of file: {e}")
        return md5_hash

    def _upload_model(self, remote_path, commit_SHA):
        _, model_name = os.path.split(self.model_full_path)
        name_before_ext, ext = tuple(os.path.splitext(model_name))
        unique_model_name = "{}_{}{}".format(name_before_ext, commit_SHA, ext)
        print(
            "Will upload {} from {} to {}".format(
                unique_model_name, self.model_full_path, remote_path
            )
        )

        upload_path = None
        try:
            if not self.algo_client.dir(remote_path).exists():
                self.algo_client.dir(remote_path).create()
            full_remote_path = "{}/{}".format(remote_path, unique_model_name)
            if self.algo_client.file(full_remote_path).exists():
                print(f"File with the same name exists, overriding: {full_remote_path}")
            result = self.algo_client.file(full_remote_path).putFile(
                self.model_full_path
            )
            if result.path:
                print(f"File successfully uploaded at: {full_remote_path}")
                upload_path = result.path
        except Exception as e:
            print(
                f"An exception occurred while uploading model file to Algorithmia: {e}"
            )
        return upload_path

    def _update_algo_model_manifest(
        self,
        git_repo,
        git_ref,
        commit_SHA,
        commit_msg,
        model_filepath,
        model_md5_hash,
        manifest_rel_path="model_manifest.json",
    ):
        manifest_full_path = f"{self.algo_name}_CI/{manifest_rel_path}"

        manifest = {}
        if os.path.exists(manifest_full_path):
            with open(manifest_full_path, "r") as manifest_file:
                manifest = json.load(manifest_file)

        manifest["model_filepath"] = model_filepath
        manifest["model_md5_hash"] = model_md5_hash
        manifest["model_origin_commit_SHA"] = commit_SHA
        manifest["model_origin_commit_msg"] = commit_msg
        manifest["model_origin_repo"] = git_repo
        manifest["model_origin_ref"] = git_ref
        manifest["model_uploaded_utc"] = datetime.utcnow().strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )

        with open(manifest_full_path, "w+") as new_manifest_file:
            json.dump(manifest, new_manifest_file)
