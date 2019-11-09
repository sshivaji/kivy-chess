from boto.ec2 import connection
import random
import datetime
from optparse import OptionParser
import dateutil.parser
from dateutil.parser import parse
import dateutil.tz as tz
import json


def start_instances(ec2conn, ident, image_name='ec2stockfish', key="stockfish", num=1, instance_type='m1.medium'):
    result = ec2conn.get_all_images(filters={'name': image_name})
    img =  result[0]
    reservation = img.run(key_name=key, min_count=num, max_count=num, instance_type=instance_type)
    for i in reservation.instances:
        i.add_tag('Name', image_name)
        i.add_tag('id', str(ident))



def get_instance(ec2conn, ident, image_prefix='ec2stockfish'):
    reservations = ec2conn.get_all_instances()
    instances = [i for r in reservations for i in r.instances]
    running_instance_list = []
    for i in instances:
        tags = i.__dict__['tags']
        # print i.dns_name
        # print dir(i)
        if tags.has_key('Name'):
            name = tags['Name']
            name = name.strip()
            # print tags
            if tags.has_key('id'):
                i_id = tags['id']
                # print i_id
                # print i.state
                # print "Name: {0}".format(name)
                # print "Image Prefix: {0}".format(image_prefix)
                # print "i_id: {0}".format(i_id)
                # print "ident: {0}".format(ident)
                if name.startswith(image_prefix) and i_id == ident:
                    # print "Found instance!"
                    return i

def get_running_instances(ec2conn, image_prefix='ec2stockfish'):
    reservations = ec2conn.get_all_instances()
    instances = [i for r in reservations for i in r.instances]
    running_instance_list = []
    for i in instances:
        tags = i.__dict__['tags']
        # print i.state
        # print i.dns_name
        # print dir(i)
        if tags.has_key('Name'):
            name = tags['Name']
            if name.startswith(image_prefix):
                d = i.__dict__
                try:
                    if d['state']!='terminated':
    #                    running_instances += 1
                        running_instance_list.append(i)
                # Instance type does not yet exist
                except KeyError:
                        running_instance_list.append(i)

    return running_instance_list

def compute_num_long_running_instances(running_instances):
    num_long_running_instances = 0
    for i in running_instances:
        launch_time = i.__dict__['launch_time']
        now = datetime.datetime.now(tz.gettz('UTC'))
        if (now - parse(launch_time).replace(tzinfo=tz.gettz('UTC'))) > datetime.timedelta(minutes=60):
            num_long_running_instances += 1
    # print "#long running instances:%d" % num_long_running_instances
    return num_long_running_instances

def process_request_api(ident, key="stockfish", instance_type="m1.medium", image_prefix = "ec2stockfish", debug=False, start=False,
                        stop=False, get_status=False, dryrun=False):
    ec2conn = connection.EC2Connection()
    ident = str(ident)
    if not dryrun:
        if get_status:
            if not ident:
                raise Exception("Need a --id option for uniquely querying image")
            i = get_instance(ec2conn, ident, image_prefix= image_prefix)
            if i:
                return {"id": ident, "state": i.state, "status": "success", "dns_name": i.dns_name}
            else:
                return {"id": ident, "state": "Not found", "status": "fail"}
                # print "id: {0}, state: {1}".format(options.id, i.state)

        # if 0 < num_instances_to_start <= options.max_instances:
        elif stop:
            if not ident:
                raise Exception("Need a --id option for terminating image")
            i = get_instance(ec2conn, ident, image_prefix= image_prefix)
            if i:
                ec2conn.terminate_instances(instance_ids=[i.id])
                return {"id": ident, "state": "terminated", "status": "success"}
            else:
                return {"status": "fail", "message": "instance not found"}
                # print "id: {0}, state: terminated".format(options.id)
        elif start:
            if not ident:
                raise Exception("Need a --id option for uniquely associating your image")
            start_instances(ec2conn, ident, image_name= image_prefix, key=key, num=1, instance_type = instance_type)
            return {"status": "success", "message": "Started instance(s)"}

        # if num_instances_to_start >=0:
        #     # Remove soft-delete tags as we need to keep instances!
        #     remove_soft_delete_instances(running_instances)

        # elif num_instances_to_start < 0:
        #     # Execute only forcestop for now, hysterisis later
        #     update_sqs_queue(options.queue, options.ctrl_queue, queue_size)
    else:
        print ("Dryrun, not doing anything")


def process_request():
    parser = OptionParser()

    parser.add_option("--key", dest='key', help="Key to use", default="stockfish")
    parser.add_option("--instance_type", dest='instance_type', help="Instance type to start.", default="m1.medium")

    parser.add_option("--image_prefix", dest='image_prefix', help="Image name prefix to use", default="ec2stockfish")
    parser.add_option("--id", dest="id", help="Unique ID for a new ec2 instance")

    parser.add_option("--debug", dest="debug", default=False, action="store_true", help="Run in debug mode")

    parser.add_option("--start", dest="start_instance", default=False, action="store_true",
        help="Start an instance")

    parser.add_option("--stop", dest="stop_instance",help="Stop an instance")
    parser.add_option("--status", dest="status", default=False, action="store_true",
        help="Get status of instance")


    parser.add_option("--dryrun", dest="dryrun", default = False, action="store_true",
        help="Dry run mode. Just report, dont do anything (don't start or trim instances).")


    options, args = parser.parse_args()
    # ec2conn = connection.EC2Connection()
    process_request_api(options.id, key=options.key, instance_type=options.instance_type,
                        image_prefix=options.image_prefix, debug=options.debug,
                        start=options.start_instance, stop=options.stop_instance, get_status=options.status, dryrun=options.dryrun)


if __name__ == '__main__':
    process_request()
