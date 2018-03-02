#!/usr/bin/python
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: ecs_service
short_description: create, terminate, start or stop a service in ecs
description:
  - Creates or terminates ecs services.
notes:
  - the service role specified must be assumable (i.e. have a trust relationship for the ecs service, ecs.amazonaws.com)
  - for details of the parameters and returns see U(http://boto3.readthedocs.org/en/latest/reference/services/ecs.html)
  - An IAM role must have been previously created
version_added: "2.1"
author:
    - "Mark Chance (@java1guy)"
    - "Darek Kaczynski (@kaczynskid)"
    - "Stephane Maarek (@simplesteph)"
    - "Zac Blazic (@zacblazic)"

requirements: [ json, botocore, boto3 ]
options:
    state:
        description:
          - The desired state of the service
        required: true
        choices: ["present", "absent", "deleting"]
    name:
        description:
          - The name of the service
        required: true
    cluster:
        description:
          - The name of the cluster in which the service exists
        required: false
    task_definition:
        description:
          - The task definition the service will run. This parameter is required when state=present
        required: false
    load_balancers:
        description:
          - The list of ELBs defined for this service
        required: false
    desired_count:
        description:
          - The count of how many instances of the service. This parameter is required when state=present
        required: false
    client_token:
        description:
          - Unique, case-sensitive identifier you provide to ensure the idempotency of the request. Up to 32 ASCII characters are allowed.
        required: false
    role:
        description:
          - The name or full Amazon Resource Name (ARN) of the IAM role that allows your Amazon ECS container agent to make calls to your load balancer
            on your behalf. This parameter is only required if you are using a load balancer with your service.
        required: false
    delay:
        description:
          - The time to wait before checking that the service is available
        required: false
        default: 10
    repeat:
        description:
          - The number of times to check that the service is available
        required: false
        default: 10
    deployment_configuration:
        description:
          - Optional parameters that control the deployment_configuration; format is '{"maximum_percent":<integer>, "minimum_healthy_percent":<integer>}
        required: false
        version_added: 2.3
    placement_constraints:
        description:
          - The placement constraints for the tasks in the service
        required: false
        version_added: 2.4
    placement_strategy:
        description:
          - The placement strategy objects to use for tasks in your service. You can specify a maximum of 5 strategy rules per service
        required: false
        version_added: 2.4
    network_configuration:
        description:
          - network configuration of the service. Only applicable for task definitions created with C(awsvpc) I(network_mode).
          - I(network_configuration) has two keys, I(subnets), a list of subnet IDs to which the task is attached and I(security_groups),
            a list of group names or group IDs for the task
        version_added: 2.5
extends_documentation_fragment:
    - aws
    - ec2
'''

EXAMPLES = '''
# Note: These examples do not set authentication details, see the AWS Guide for details.
- ecs_service:
    state: present
    name: console-test-service
    cluster: new_cluster
    task_definition: 'new_cluster-task:1'
    desired_count: 0

# Basic provisioning example
- ecs_service:
    name: default
    state: present
    cluster: new_cluster

- name: create ECS service on VPC network
  ecs_service:
    state: present
    name: console-test-service
    cluster: new_cluster
    task_definition: 'new_cluster-task:1'
    desired_count: 0
    network_configuration:
      subnets:
      - subnet-abcd1234
      security_groups:
      - sg-aaaa1111
      - my_security_group

# Simple example to delete
- ecs_service:
    name: default
    state: absent
    cluster: new_cluster

# With custom deployment configuration (added in version 2.3), placement constraints and strategy (added in version 2.4)
- ecs_service:
    state: present
    name: test-service
    cluster: test-cluster
    task_definition: test-task-definition
    desired_count: 3
    deployment_configuration:
      minimum_healthy_percent: 75
      maximum_percent: 150
    placement_constraints:
      - type: memberOf
        expression: 'attribute:flavor==test'
    placement_strategy:
      - type: binpack
        field: memory
'''

RETURN = '''
service:
    description: Details of created service.
    returned: when creating a service
    type: complex
    contains:
        clusterArn:
            description: The Amazon Resource Name (ARN) of the of the cluster that hosts the service.
            returned: always
            type: string
        desiredCount:
            description: The desired number of instantiations of the task definition to keep running on the service.
            returned: always
            type: int
        loadBalancers:
            description: A list of load balancer objects
            returned: always
            type: complex
            contains:
                loadBalancerName:
                    description: the name
                    returned: always
                    type: string
                containerName:
                    description: The name of the container to associate with the load balancer.
                    returned: always
                    type: string
                containerPort:
                    description: The port on the container to associate with the load balancer.
                    returned: always
                    type: int
        pendingCount:
            description: The number of tasks in the cluster that are in the PENDING state.
            returned: always
            type: int
        runningCount:
            description: The number of tasks in the cluster that are in the RUNNING state.
            returned: always
            type: int
        serviceArn:
            description: The Amazon Resource Name (ARN) that identifies the service. The ARN contains the arn:aws:ecs namespace, followed by the region
                         of the service, the AWS account ID of the service owner, the service namespace, and then the service name. For example,
                         arn:aws:ecs:region :012345678910 :service/my-service .
            returned: always
            type: string
        serviceName:
            description: A user-generated string used to identify the service
            returned: always
            type: string
        status:
            description: The valid values are ACTIVE, DRAINING, or INACTIVE.
            returned: always
            type: string
        taskDefinition:
            description: The ARN of a task definition to use for tasks in the service.
            returned: always
            type: string
        deployments:
            description: list of service deployments
            returned: always
            type: list of complex
        deploymentConfiguration:
            description: dictionary of deploymentConfiguration
            returned: always
            type: complex
            contains:
                maximumPercent:
                    description: maximumPercent param
                    returned: always
                    type: int
                minimumHealthyPercent:
                    description: minimumHealthyPercent param
                    returned: always
                    type: int
        events:
            description: list of service events
            returned: always
            type: list of complex
        placementConstraints:
            description: List of placement constraints objects
            returned: always
            type: list of complex
            contains:
                type:
                    description: The type of constraint. Valid values are distinctInstance and memberOf.
                    returned: always
                    type: string
                expression:
                    description: A cluster query language expression to apply to the constraint. Note you cannot specify an expression if the constraint type is
                                 distinctInstance.
                    returned: always
                    type: string
        placementStrategy:
            description: List of placement strategy objects
            returned: always
            type: list of complex
            contains:
                type:
                    description: The type of placement strategy. Valid values are random, spread and binpack.
                    returned: always
                    type: string
                field:
                    description: The field to apply the placement strategy against. For the spread placement strategy, valid values are instanceId
                                 (or host, which has the same effect), or any platform or custom attribute that is applied to a container instance,
                                 such as attribute:ecs.availability-zone. For the binpack placement strategy, valid values are CPU and MEMORY.
                    returned: always
                    type: string
ansible_facts:
    description: Facts about deleted service.
    returned: when deleting a service
    type: complex
    contains:
        service:
            description: Details of deleted service in the same structure described above for service creation.
            returned: when service existed and was deleted
            type: complex
'''
import time

DEPLOYMENT_CONFIGURATION_TYPE_MAP = {
    'maximum_percent': 'int',
    'minimum_healthy_percent': 'int'
}

from ansible.module_utils.aws.core import AnsibleAWSModule
from ansible.module_utils.ec2 import boto3_conn, ec2_argument_spec, get_aws_connection_info
from ansible.module_utils.ec2 import snake_dict_to_camel_dict, map_complex_type, get_ec2_security_group_ids_from_names

try:
    import botocore
except ImportError:
    pass  # handled by AnsibleAWSModule


class EcsServiceManager:
    """Handles ECS Services"""

    def __init__(self, module):
        self.module = module
        region, ec2_url, aws_connect_kwargs = get_aws_connection_info(module, boto3=True)
        self.ecs = boto3_conn(module, conn_type='client', resource='ecs', region=region, endpoint=ec2_url, **aws_connect_kwargs)
        self.ec2 = boto3_conn(module, conn_type='client', resource='ec2', region=region, endpoint=ec2_url, **aws_connect_kwargs)

    def format_network_configuration(self, network_config):
        result = dict()
        if 'subnets' in network_config:
            result['subnets'] = network_config['subnets']
        else:
            self.module.fail_json(msg="Network configuration must include subnets")
        if 'security_groups' in network_config:
            groups = network_config['security_groups']
            if any(not sg.startswith('sg-') for sg in groups):
                try:
                    vpc_id = self.ec2.describe_subnets(SubnetIds=[result['subnets'][0]])['Subnets'][0]['VpcId']
                    groups = get_ec2_security_group_ids_from_names(groups, self.ec2, vpc_id)
                except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
                    self.module.fail_json_aws(e, msg="Couldn't look up security groups")
            result['securityGroups'] = groups
        return dict(awsvpcConfiguration=result)

    def find_in_array(self, array_of_services, service_name, field_name='serviceArn'):
        for c in array_of_services:
            if c[field_name].endswith(service_name):
                return c
        return None

    def describe_service(self, cluster_name, service_name):
        try:
            response = self.ecs.describe_services(
                cluster=cluster_name,
                services=[service_name])
        except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
            self.module.fail_json_aws(e, msg="Couldn't describe ECS service")
        msg = ''
        if len(response['failures']) > 0:
            c = self.find_in_array(response['failures'], service_name, 'arn')
            msg += ", failure reason is " + c['reason']
            if c and c['reason'] == 'MISSING':
                return None
            # fall thru and look through found ones
        if len(response['services']) > 0:
            c = self.find_in_array(response['services'], service_name)
            if c:
                return c
        raise Exception("Unknown problem describing service %s." % service_name)

    def is_matching_service(self, expected, existing):
        if expected['task_definition'] != existing['taskDefinition']:
            return False

        if (expected['load_balancers'] or []) != existing['loadBalancers']:
            return False

        if (expected['desired_count'] or 0) != existing['desiredCount']:
            return False

        return True

    def create_service(self, service_name, cluster_name, task_definition, load_balancers,
                       desired_count, client_token, role, deployment_configuration,
                       placement_constraints, placement_strategy, network_configuration):
        params = dict(
            cluster=cluster_name,
            serviceName=service_name,
            taskDefinition=task_definition,
            loadBalancers=load_balancers,
            desiredCount=desired_count,
            clientToken=client_token,
            role=role,
            deploymentConfiguration=deployment_configuration,
            placementConstraints=placement_constraints,
            placementStrategy=placement_strategy)
        if network_configuration:
            params['networkConfiguration'] = network_configuration
        try:
            response = self.ecs.create_service(**params)
        except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
            self.module.fail_json_aws(e, msg="Couldn't create ECS service")
        return response['service']

    def update_service(self, service_name, cluster_name, task_definition,
                       desired_count, deployment_configuration, network_configuration):
        params = dict(
            cluster=cluster_name,
            service=service_name,
            taskDefinition=task_definition,
            desiredCount=desired_count,
            deploymentConfiguration=deployment_configuration)
        if network_configuration:
            params['networkConfiguration'] = network_configuration
        try:
            response = self.ecs.update_service(**params)
        except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
            self.module.fail_json_aws(e, msg="Couldn't update ECS service")
        return response['service']

    def delete_service(self, service, cluster=None):
        try:
            return self.ecs.delete_service(cluster=cluster, service=service)
        except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
            self.module.fail_json_aws(e, msg="Couldn't delete ECS service")

    def ecs_api_handles_network_configuration(self):
        from distutils.version import LooseVersion
        # There doesn't seem to be a nice way to inspect botocore to look
        # for attributes (and networkConfiguration is not an explicit argument
        # to e.g. ecs.run_task, it's just passed as a keyword argument)
        return LooseVersion(botocore.__version__) >= LooseVersion('1.7.44')


def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(
        state=dict(required=True, choices=['present', 'absent', 'deleting']),
        name=dict(required=True, type='str'),
        cluster=dict(required=False, type='str'),
        task_definition=dict(required=False, type='str'),
        load_balancers=dict(required=False, default=[], type='list'),
        desired_count=dict(required=False, type='int'),
        client_token=dict(required=False, default='', type='str'),
        role=dict(required=False, default='', type='str'),
        delay=dict(required=False, type='int', default=10),
        repeat=dict(required=False, type='int', default=10),
        deployment_configuration=dict(required=False, default={}, type='dict'),
        placement_constraints=dict(required=False, default=[], type='list'),
        placement_strategy=dict(required=False, default=[], type='list'),
        network_configuration=dict(required=False, type='dict')
    ))

    module = AnsibleAWSModule(argument_spec=argument_spec,
                              supports_check_mode=True,
                              required_if=[('state', 'present', ['task_definition', 'desired_count'])],
                              required_together=[['load_balancers', 'role']])

    service_mgr = EcsServiceManager(module)
    if module.params['network_configuration']:
        if not service_mgr.ecs_api_handles_network_configuration():
            module.fail_json(msg='botocore needs to be version 1.7.44 or higher to use network configuration')
        network_configuration = service_mgr.format_network_configuration(module.params['network_configuration'])
    else:
        network_configuration = None

    deployment_configuration = map_complex_type(module.params['deployment_configuration'],
                                                DEPLOYMENT_CONFIGURATION_TYPE_MAP)

    deployment_configuration = snake_dict_to_camel_dict(deployment_configuration)

    try:
        existing = service_mgr.describe_service(module.params['cluster'], module.params['name'])
    except Exception as e:
        module.fail_json(msg="Exception describing service '" + module.params['name'] + "' in cluster '" + module.params['cluster'] + "': " + str(e))

    results = dict(changed=False)
    if module.params['state'] == 'present':

        matching = False
        update = False
        if existing and 'status' in existing and existing['status'] == "ACTIVE":
            if service_mgr.is_matching_service(module.params, existing):
                matching = True
                results['service'] = existing
            else:
                update = True

        if not matching:
            if not module.check_mode:

                role = module.params['role']
                client_token = module.params['client_token']
                load_balancers = module.params['load_balancers']

                if update:
                    if (existing['loadBalancers'] or []) != load_balancers:
                        module.fail_json(msg="It is not possible to update the load balancers of an existing service")
                    # update required
                    response = service_mgr.update_service(module.params['name'],
                                                          module.params['cluster'],
                                                          module.params['task_definition'],
                                                          module.params['desired_count'],
                                                          deployment_configuration,
                                                          network_configuration)
                else:
                    for load_balancer in load_balancers:
                        if 'containerPort' in load_balancer:
                            load_balancer['containerPort'] = int(load_balancer['containerPort'])
                    # doesn't exist. create it.
                    response = service_mgr.create_service(module.params['name'],
                                                          module.params['cluster'],
                                                          module.params['task_definition'],
                                                          load_balancers,
                                                          module.params['desired_count'],
                                                          client_token,
                                                          role,
                                                          deployment_configuration,
                                                          module.params['placement_constraints'],
                                                          module.params['placement_strategy'],
                                                          network_configuration)

                results['service'] = response

            results['changed'] = True

    elif module.params['state'] == 'absent':
        if not existing:
            pass
        else:
            # it exists, so we should delete it and mark changed.
            # return info about the cluster deleted
            del existing['deployments']
            del existing['events']
            results['ansible_facts'] = existing
            if 'status' in existing and existing['status'] == "INACTIVE":
                results['changed'] = False
            else:
                if not module.check_mode:
                    try:
                        service_mgr.delete_service(
                            module.params['name'],
                            module.params['cluster']
                        )
                    except botocore.exceptions.ClientError as e:
                        module.fail_json(msg=e.message)
                results['changed'] = True

    elif module.params['state'] == 'deleting':
        if not existing:
            module.fail_json(msg="Service '" + module.params['name'] + " not found.")
            return
        # it exists, so we should delete it and mark changed.
        # return info about the cluster deleted
        delay = module.params['delay']
        repeat = module.params['repeat']
        time.sleep(delay)
        for i in range(repeat):
            existing = service_mgr.describe_service(module.params['cluster'], module.params['name'])
            status = existing['status']
            if status == "INACTIVE":
                results['changed'] = True
                break
            time.sleep(delay)
        if i is repeat - 1:
            module.fail_json(msg="Service still not deleted after " + str(repeat) + " tries of " + str(delay) + " seconds each.")
            return

    module.exit_json(**results)


if __name__ == '__main__':
    main()
