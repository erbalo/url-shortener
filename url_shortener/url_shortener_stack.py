from aws_cdk import (
    aws_dynamodb,
    aws_lambda,
    aws_apigateway,
    aws_ec2 as ec2,
    core as cdk,
)

from cdk_watchful import Watchful


class UrlShortenerStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(
            self,
            "test-vpc-url",
            cidr="12.3.0.0/16",
            max_azs=2,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            nat_gateway_provider=ec2.NatProvider.gateway(),
            nat_gateways=1,
        )

        table = aws_dynamodb.Table(
            self,
            "test-mapping-table",
            partition_key=aws_dynamodb.Attribute(
                name="id", type=aws_dynamodb.AttributeType.STRING
            ),
        )

        function = aws_lambda.Function(
            self,
            "test-backend",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            handler="handler.main",
            code=aws_lambda.Code.asset("./lambda"),
            vpc=vpc
        )

        table.grant_read_write_data(function)
        function.add_environment("TABLE_NAME", table.table_name)

        api = aws_apigateway.LambdaRestApi(self, "test-api", handler=function)

        wf = Watchful(self, "monitoring", alarm_email="erick.barrera@casai.com")
        wf.watch_scope(self)
