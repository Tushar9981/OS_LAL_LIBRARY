#ifndef OSLAL_H
#define OSLAL_H

typedef struct {
    double priority;
    double req_bandwidth_mbps;
    double max_latency_ms;
} oslal_policy_t;

int oslal_init(void);
int oslal_bind_socket(int socket_fd, oslal_policy_t policy);

#endif
