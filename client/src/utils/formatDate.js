export const formatDate = (isoDate) => {
  const dateObject = new Date(isoDate);
  const day = String(dateObject.getDate()).padStart(2, "0");
  const month = String(dateObject.getMonth() + 1).padStart(2, "0"); // Month is zero-based
  const year = dateObject.getFullYear();

  return `${day}/${month}/${year}`;
};
