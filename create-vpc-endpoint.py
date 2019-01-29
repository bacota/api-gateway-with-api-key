import boto3
import sys

if len(sys.argv) != 3:
    print(f"usage {sys.argv[0]} vpc-id region")
    exit(0)

vpcId = sys.argv[1]
region = sys.argv[2]

ec2 = boto3.client('ec2', region_name=region)

rts = ec2.describe_route_tables(Filters = [ { 'Name' : 'vpc-id', 'Values' : [vpcId] }  ])['RouteTables']
rtIds = list(map(lambda t: t['RouteTableId'], rts))

ec2.create_vpc_endpoint(
    VpcEndpointType='Gateway',
    ServiceName= f'com.amazonaws.{region}.s3',
    VpcId = vpcId,
    RouteTableIds = rtIds
)

print('Created')

                                     
