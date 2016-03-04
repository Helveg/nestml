/*
 * Copyright (c) 2015 RWTH Aachen. All rights reserved.
 *
 * http://www.se-rwth.de/
 */
package org.nest.integration;

import org.junit.Ignore;
import org.junit.Test;
import org.nest.base.ModelbasedTest;
import org.nest.codegeneration.sympy.SymPyScriptEvaluator;
import org.nest.codegeneration.sympy.ODESolverScriptGenerator;
import org.nest.nestml._ast.ASTNESTMLCompilationUnit;
import org.nest.nestml._symboltable.NESTMLScopeCreator;

import java.io.IOException;
import java.nio.file.Path;
import java.util.Optional;

import static org.junit.Assert.assertTrue;

/**
 * Test evaluation of the solver script. Depends on successful script generation.
 *
 * @author plonikov
 */
public class SymPyScriptEvaluatorTest extends ModelbasedTest {
  private static final String PSC_MODEL_FILE
      = "src/test/resources/codegeneration/iaf_neuron.nestml";
  private static final String COND_MODEL_FILE
      = "src/test/resources/codegeneration/iaf_cond_alpha.nestml";

  @Test
  public void generateAndExecuteSympyScriptForPSC() throws IOException {
    generateAndEvaluate(PSC_MODEL_FILE);
  }

  @Test
  public void generateAndExecuteSympyScriptForCOND() throws IOException {
    generateAndEvaluate(COND_MODEL_FILE);
  }

  private void generateAndEvaluate(final String pathToModel) throws IOException {
    final Optional<ASTNESTMLCompilationUnit> root = parser.parse(pathToModel);

    assertTrue(root.isPresent());

    final NESTMLScopeCreator nestmlScopeCreator = new NESTMLScopeCreator(TEST_MODEL_PATH);
    nestmlScopeCreator.runSymbolTableCreator(root.get());

    final Optional<Path> generatedScript = ODESolverScriptGenerator.generateSympyODEAnalyzer(
        root.get().getNeurons().get(0),
        OUTPUT_FOLDER);

    assertTrue(generatedScript.isPresent());
    final SymPyScriptEvaluator evaluator = new SymPyScriptEvaluator();

    assertTrue(evaluator.execute(generatedScript.get()));
  }

}
