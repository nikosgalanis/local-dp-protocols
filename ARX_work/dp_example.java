/*
 * ARX: Powerful Data Anonymization
 * Copyright 2012 - 2020 Fabian Prasser and contributors
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 * http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.deidentifier.arx.examples;
import java.util.Iterator;

import java.io.IOException;

import java.nio.charset.Charset;


import org.deidentifier.arx.ARXAnonymizer;
import org.deidentifier.arx.ARXConfiguration;
import org.deidentifier.arx.ARXResult;
import org.deidentifier.arx.AttributeType;
import org.deidentifier.arx.AttributeType.Hierarchy;
import org.deidentifier.arx.Data;
import org.deidentifier.arx.Data.DefaultData;
import org.deidentifier.arx.DataGeneralizationScheme;
import org.deidentifier.arx.DataGeneralizationScheme.GeneralizationDegree;
import org.deidentifier.arx.DataHandle;
import org.deidentifier.arx.DataType;
import org.deidentifier.arx.criteria.EDDifferentialPrivacy;
import java.nio.charset.StandardCharsets;

/**
 * This class implements an example on how to use the API by directly providing
 * the input datasets.
 *
 * @author Fabian Prasser
 * @author Florian Kohlmayer
 */
public class dp_example extends Example {

    /**
     * Entry point.
     * 
     * @param args
     *            the arguments
     * @throws IOException 
     */
	
	protected static double run_query(ARXResult data, int targetColumn) {
		// iterator that we are going to use to access the data
		final Iterator<String[]> itHandle = data.getOutput().iterator();
		
		// result of the query
		double result = 0d;
		// length of the dataset
		int totalRecords = 0;
		
		// get the first element of the column, thus the name of it, and ignore it
		String[] name = itHandle.next();
		if (name.length <= targetColumn) {
			System.out.println("Target column out of bounds\n");
			return 0d;
		}

		// iterate through all the values in the dataset
		while(itHandle.hasNext()) {
			String[] next = itHandle.next();
			// check that our target position is legal
			String string = next[targetColumn];
			if (!string.equals("*")) {
				result += Integer.parseInt(string);		
				totalRecords++;				
			}
		}
//    	System.out.println(result);
		return result / totalRecords;
	}
	
    public static void main(String[] args) throws IOException {

        // import the data
        Data data = Data.create("data/nba/new_salaries.csv", StandardCharsets.UTF_8, ',');

        // set the hierarchies for each column 
        Hierarchy position = Hierarchy.create("data/nba/position_hierarchy.csv", StandardCharsets.UTF_8, ',');
        Hierarchy year = Hierarchy.create("data/nba/year_hierarchy.csv", StandardCharsets.UTF_8, ',');
        Hierarchy age = Hierarchy.create("data/nba/age_hierarchy.csv", StandardCharsets.UTF_8, ',');
        Hierarchy team = Hierarchy.create("data/nba/team_hierarchy.csv", StandardCharsets.UTF_8, ';');
        Hierarchy salary = Hierarchy.create("data/nba/salaries_hierarchy.csv", StandardCharsets.UTF_8, ',');

        
        data.getDefinition().setAttributeType("Pos", AttributeType.INSENSITIVE_ATTRIBUTE);
        data.getDefinition().setAttributeType("Year", AttributeType.INSENSITIVE_ATTRIBUTE);
        data.getDefinition().setAttributeType("Age", AttributeType.INSENSITIVE_ATTRIBUTE);
        data.getDefinition().setAttributeType("Tm", AttributeType.QUASI_IDENTIFYING_ATTRIBUTE);
        data.getDefinition().setAttributeType("Salary", AttributeType.QUASI_IDENTIFYING_ATTRIBUTE);// AttributeType.IDENTIFYING_ATTRIBUTE);
        
        data.getDefinition().setHierarchy("Pos", position);
        data.getDefinition().setHierarchy("Year", year);
        data.getDefinition().setHierarchy("Age", age);
        data.getDefinition().setHierarchy("Tm", team);
        data.getDefinition().setHierarchy("Salary", salary);
        
         // Create an instance of the anonymizer

        // Create a differential privacy criterion
        // we want (1,0) - DP
        // delta is suggested to be 1/#records
        double total_res = 0d;
        int solved = 0;
        for (int i = 0; i < 500; i++) {
        	data.getHandle().release();
        	
        	System.out.println(i);

        	ARXAnonymizer anonymizer = new ARXAnonymizer();
        	
        	EDDifferentialPrivacy criterion = new EDDifferentialPrivacy(1.7d, 1d / data.getHandle().getNumRows());
        	
        	ARXConfiguration config = ARXConfiguration.create();
        	config.addPrivacyModel(criterion);
        	config.setSuppressionLimit(1d);
            config.setHeuristicSearchStepLimit(100);
            ARXResult result = anonymizer.anonymize(data, config);
        	     
        	double res = run_query(result, 4);
//            printResult(result, data);

        	if (res > 0) {
//            	System.out.print("--------------------------------" + res);

        		total_res += res;
        		solved++;
        	}
        }
        total_res /= solved;
    	System.out.print("Total result " + total_res);
    }
}
