package ch.heigvd.cld.lab;

import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Enumeration;

@WebServlet(name = "DatastoreWrite", value = "/datastorewrite")
public class DatastoreWrite extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws IOException {

        resp.setContentType("text/plain");
        PrintWriter pw = resp.getWriter();

        String kind = req.getParameter("_kind");
        if (kind == null) {
            pw.println("Error: _kind parameter is missing");
            resp.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }

        // Handle optional _key parameter
        String keyName = req.getParameter("_key");
        Entity entity;
        if (keyName != null) {
            entity = new Entity(kind, keyName);
        } else {
            entity = new Entity(kind);
        }

        // Iterate through all parameter names to set entity properties
        Enumeration<String> parameterNames = req.getParameterNames();
        while (parameterNames.hasMoreElements()) {
            String paramName = parameterNames.nextElement();
            // Skip the special parameters _kind and _key
            if (paramName.equals("_kind") || paramName.equals("_key")) continue;

            String paramValue = req.getParameter(paramName);
            entity.setProperty(paramName, paramValue);
        }

        // Write the entity to the datastore
        DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
        datastore.put(entity);
        pw.println("Entity written to datastore with kind " + kind +
                (keyName != null ? " and key " + keyName : " and autogenerated key"));
    }
}
