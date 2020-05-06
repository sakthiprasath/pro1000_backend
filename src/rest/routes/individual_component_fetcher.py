from flask_rest_api import Blueprint
import  flask
from flask import jsonify , after_this_request
from flask import request
import json
from src.sql_modules.sql_individual_component_fetch import  SQLIndividualComponent
from src.utils.database_connection_manager import get_test_tenant_details


individual_component_fetcher_routes = Blueprint('individual_component_fetcher', __name__, url_prefix='/api/individual-component-fetch')


@individual_component_fetcher_routes.route('<component_key>', methods=['GET'])
# @tenant_config_routes.response(TenantConfigSchema(many=True), code=200)
@individual_component_fetcher_routes.doc(summary='Get all settings for the Tenant',
                                         description='Returns list of all settings with key and value string')
def fetch_individual_component_codes(component_key):
    @after_this_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    try:
        #tenant_db_name, schema_name, tenant_id, tenant_name = get_test_tenant_details()
        file_contents = SQLIndividualComponent().get_all_configs(component_key)
        return jsonify(file_contents)
    except Exception as e:
        return print(e)

@individual_component_fetcher_routes.route('', methods=['GET'])
def return_index_html():
    try:
       return  flask.render_template('CompanyProRecover.html')
    except Exception as e:
        return print(e)

@individual_component_fetcher_routes.route('save-file/<file_name>', methods=['POST'])
def save_file(file_name):
    try:
        data = request.get_json()
        SQLIndividualComponent().result_write(file_name,data)
    except Exception as e:
        return print(e)

@individual_component_fetcher_routes.route('/general_files/<file_name>', methods=['GET'])
def get_data_by_name(file_name):
    @after_this_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    try:
        file_data = SQLIndividualComponent().get_file_data(file_name)
        return file_data
    except Exception as e:
        return print(e)


