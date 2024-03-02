const filterByFirstName = (customers, searchQuery) => {
  return customers.filter((customer) =>
    customer.first_name.toLowerCase().includes(searchQuery.toLowerCase())
  );
};

const filterByLastName = (customers, searchQuery) => {
  return customers.filter((customer) =>
    customer.last_name.toLowerCase().includes(searchQuery.toLowerCase())
  );
};

const filterByPhoneNumber = (customers, searchQuery) => {
  return customers.filter((customer) =>
    customer.phone_number.includes(searchQuery)
  );
};

const filterByAddress = (customers, searchQuery) => {
  return customers.filter((customer) =>
    customer.address.toLowerCase().includes(searchQuery.toLowerCase())
  );
};

const filterByService = (customers, searchQuery) => {
  return customers.filter((customer) =>
    customer.services.some((service) =>
      service.name.toLowerCase().includes(searchQuery.toLowerCase())
    )
  );
};

export const filters = {
  filterByFirstName,
  filterByLastName,
  filterByPhoneNumber,
  filterByAddress,
  filterByService,
};
