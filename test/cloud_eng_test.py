from boto.ec2 import connection
import random
import datetime
from optparse import OptionParser
from dateutil.parser import parse
import dateutil.tz as tz


def start_instances(ec2conn, image_name='ec2stockfish', key="stockfish", num=1, instance_type='m1.medium'):
    result = ec2conn.get_all_images(filters={'name': image_name})
    img =  result[0]
    reservation = img.run(key_name=key, min_count=num, max_count=num, instance_type=instance_type)
    for i in reservation.instances:
        i.add_tag('Name', image_name)


def get_instance(ec2conn, id, image_prefix='ec2stockfish'):
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
            # print name
            # print tags
            if tags.has_key('id'):
                i_id = tags['id']
                if name.startswith(image_prefix) and i_id == id:
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
    parser.add_option("--status", dest="status",
        help="Get status of instance")


    parser.add_option("--dryrun", dest="dryrun", default = False, action="store_true",
        help="Dry run mode. Just report, dont do anything (don't start or trim instances).")


    options, args = parser.parse_args()
    ec2conn = connection.EC2Connection()

#    print "get_num_running"
    running_instances = get_running_instances(ec2conn, image_prefix=options.image_prefix)
    # print "running_instances:"
    # print running_instances
    num_long_running_instances = compute_num_long_running_instances(running_instances)
    num_running_instances = len(running_instances)
    # print ec2conn.get_all_images(filters={'name': 'HighCPU'})



#    print "get_queue_size"
#     queue_size = get_queue_size(options.queue)
#    print "get_num_instance_to_start_stop"
#     num_instances_to_start = get_num_instances_to_start_or_stop(queue_size, num_running_instances, ratio = options.ratio, max = options.max_instances, debug=options.debug)

    # There are more than 1 long running instance
    # if num_long_running_instances > 0 and queue_size>0:
    #     num_instances_to_start+=num_long_running_instances
    #     if num_instances_to_start + num_running_instances > options.max_instances:
    #         num_instances_to_start = options.max_instances - num_running_instances
    #
    # print "Queue size: %d"%queue_size
    # print "Num of instances to spin up: %d"%num_instances_to_start
    # print "Running_instances: %d"%num_running_instances

    if not options.dryrun:
        if options.status:
            if not options.id:
                raise Exception("Need a --id option for uniquely querying image")
            i = get_instance(ec2conn,options.id, image_prefix=options.image_prefix)
            if i:
                print "id: {0}, state: {1}".format(options.id, i.state)

        # if 0 < num_instances_to_start <= options.max_instances:
        elif options.stop_instance:
            if not options.id:
                raise Exception("Need a --id option for terminating image")
            i = get_instance(ec2conn,options.id, image_prefix=options.image_prefix)
            if i:
                ec2conn.terminate_instances(instance_ids=[i.id])
                print "id: {0}, state: terminated".format(options.id)
        elif options.start_instance:
            if not options.id:
                raise Exception("Need a --id option for uniquely associating your image")
            start_instances(ec2conn, image_name=options.image_prefix, key = options.key, num = 1, instance_type = options.instance_type)

        # if num_instances_to_start >=0:
        #     # Remove soft-delete tags as we need to keep instances!
        #     remove_soft_delete_instances(running_instances)

        # elif num_instances_to_start < 0:
        #     # Execute only forcestop for now, hysterisis later
        #     update_sqs_queue(options.queue, options.ctrl_queue, queue_size)
    else:
        print "Dryrun, not doing anything"
if __name__ == '__main__':
    process_request()