import http from 'k6/http';

export default function() {
  var hostname = __ENV.APP_HOSTNAME || "localhost:8000"
  var server_list = [hostname]
  var endpoint_list = ["/", "/io_task", "/cpu_task", "/random_sleep", "/random_status", "/chain", "/error_test"]
  server_list.forEach(function(server) {
    endpoint_list.forEach(function(endpoint) {
      http.get(`http://${server}${endpoint}`);
    });
  });
}
