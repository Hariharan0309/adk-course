import os
import shutil
from datetime import datetime
from typing import Optional, List, Dict, Any
import vertexai
from vertexai.agent_engines import AdkApp

# Import the standard ADK components directly from the library
from google.adk.cli.cli_deploy import (
    _AGENT_ENGINE_APP_TEMPLATE, 
    _AGENT_ENGINE_CLASS_METHODS,  # This is the standard list of methods
    _resolve_project
)

def deploy_to_vertex_agent_engine(
    agent_folder: str,
    project: str,
    region: str,
    staging_bucket: str,
    display_name: Optional[str] = None,
    description: Optional[str] = None,
    agent_engine_id: Optional[str] = None,
    custom_methods: Optional[List[Dict[str, Any]]] = None
):
    """
    Custom deployment script for Vertex AI Agent Engine.
    Imports standard methods from ADK and appends custom ones.
    """
    
    agent_folder = os.path.abspath(agent_folder)
    app_name = os.path.basename(agent_folder)
    display_name = display_name or app_name
    parent_folder = os.path.dirname(agent_folder)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    temp_folder = f"{app_name}_deploy_{timestamp}"
    staging_path = os.path.join(parent_folder, temp_folder)
    
    print(f"--- Starting Custom Deployment ---")
    print(f"Staging files in: {staging_path}")
    
    if os.path.exists(staging_path):
        shutil.rmtree(staging_path)

    try:
        shutil.copytree(agent_folder, staging_path)
        
        # Ensure requirements.txt exists
        req_path = os.path.join(staging_path, 'requirements.txt')
        if not os.path.exists(req_path):
            with open(req_path, 'w') as f:
                f.write('google-cloud-aiplatform[adk,agent_engines]\n')
        
        # Prepare the entrypoint file
        adk_app_file = os.path.join(staging_path, 'ae_entrypoint.py')
        with open(adk_app_file, 'w') as f:
            f.write(_AGENT_ENGINE_APP_TEMPLATE.format(
                app_name=app_name,
                trace_to_cloud_option=True,
                is_config_agent=os.path.exists(os.path.join(staging_path, 'root_agent.yaml')),
                temp_folder=temp_folder,
                agent_folder=agent_folder,
                adk_app_object='root_agent',
                adk_app_type='agent',
                express_mode=False
            ))

        vertexai.init(project=project, location=region)
        client = vertexai.Client(project=project, location=region)
        
        agent_config = {
            'display_name': display_name,
            'description': description or "ADK Agent deployed via custom script",
            'staging_bucket': staging_bucket,
            'requirements_file': f"{temp_folder}/requirements.txt",
            'entrypoint_module': f"{temp_folder}.ae_entrypoint",
            'entrypoint_object': 'adk_app',
            'source_packages': [temp_folder],
            'agent_framework': 'google-adk'
        }

        # MERGE METHODS: Start with standard ones, then add yours
        final_methods = list(_AGENT_ENGINE_CLASS_METHODS)
        if custom_methods:
            print(f"Adding {len(custom_methods)} custom methods to the standard set...")
            final_methods.extend(custom_methods)
        
        agent_config['class_methods'] = final_methods

        if not agent_engine_id:
            print("Creating new Agent Engine instance...")
            agent_engine = client.agent_engines.create(config=agent_config)
            print(f"✅ Created: {agent_engine.api_resource.name}")
        else:
            if not agent_engine_id.startswith('projects/'):
                full_id = f"projects/{project}/locations/{region}/reasoningEngines/{agent_engine_id}"
            else:
                full_id = agent_engine_id
            print(f"Updating instance: {full_id}")
            client.agent_engines.update(name=full_id, config=agent_config)
            print(f"✅ Updated: {full_id}")

    finally:
        print(f"Cleaning up: {staging_path}")
        shutil.rmtree(staging_path)

if __name__ == "__main__":
    # --- CONFIGURATION ---
    PROJECT_ID = "YOUR_PROJECT_ID"
    LOCATION = "us-central1"
    BUCKET = "gs://YOUR_STAGING_BUCKET"
    AGENT_DIR = "./myAgent"
    
    # --- CUSTOM METHODS ---
    MY_CUSTOM_METHODS = [
        # {
        #     'name': 'my_custom_operation',
        #     'description': 'Description here',
        #     'parameters': { ... },
        #     'api_mode': 'async',
        # }
    ]

    deploy_to_vertex_agent_engine(
        agent_folder=AGENT_DIR,
        project=PROJECT_ID,
        region=LOCATION,
        staging_bucket=BUCKET,
        custom_methods=MY_CUSTOM_METHODS
    )
