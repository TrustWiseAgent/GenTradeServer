"""
Utils
"""
import logging
import ntplib

LOG = logging.getLogger(__name__)

def check_server_time() -> float:
    """
    Sync with NTP server

    :return : offset in seconds
    """
    ntp_servers = ['ntp.ntsc.ac.cn', 'ntp.sjtu.edu.cn', 'cn.ntp.org.cn',
                   'cn.pool.ntp.org', 'ntp.aliyun.com']
    retry = len(ntp_servers) - 1
    client = ntplib.NTPClient()
    while retry > 0:
        LOG.info("Try to get time from NTP: %s", ntp_servers[retry])

        try:
            ret = client.request(ntp_servers[retry], version=3)
            offset = (ret.recv_time - ret.orig_time +
                    ret.dest_time - ret.tx_time) / 2
            LOG.info("NTP offset: %.2f seconds", offset)
            return offset
        except ntplib.NTPException:
            LOG.error("Fail to get time, try another")
            retry -= 1
            continue
    return None
