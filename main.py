import os

from ams.BaseService import BaseService
from traffic_ops.TmWrapper import TmWrapper
from traffic_ops.ToWrapper import ToWrapper


def main():
    wrapper = ToWrapper(os.environ['TO_SERVER'], port=443, user=os.environ['TO_USER'], password=os.environ['TO_PASSWORD'])
    svc = BaseService(wrapper, TmWrapper())
    svc.start()


if __name__ == "__main__":
    main()